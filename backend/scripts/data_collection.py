# ...existing code...
# If you're in Colab, uncomment:
# !pip install -q datasets

from datasets import load_dataset, Dataset
# ...existing code...

# ---------------------------------------------------
# 1. Define skin / skincare / dermatology keywords
# ---------------------------------------------------
SKIN_KEYWORDS = [
    # general
    "skin", "skincare", "skin care", "dermatology", "dermatologist",
    "rash", "rashes", "itch", "itchy", "pruritus",
    "allergy", "allergic reaction", "hives", "urticaria",

    # acne & oil control
    "acne", "pimple", "pimples", "blackheads", "whiteheads",
    "comedone", "oily skin", "seborrheic", "seborrheic dermatitis",
    "sebum",

    # pigmentation & cosmetic
    "melasma", "hyperpigmentation", "dark spots", "dark spot",
    "pigmentation", "freckle", "freckles", "age spots",
    "vitiligo", "albinism",

    # eczema / dermatitis / psoriasis / rosacea
    "eczema", "atopic dermatitis", "contact dermatitis",
    "psoriasis", "rosacea", "seborrhea",

    # infections & lesions
    "impetigo", "ringworm", "tinea", "fungal infection",
    "athlete's foot", "jock itch", "scabies", "warts",
    "mole", "nevus", "lesion", "skin cancer", "melanoma",
    "basal cell", "squamous cell carcinoma",

    # sun & products
    "sunscreen", "spf", "sunblock", "sunburn",
    "moisturizer", "moisturiser", "retinol", "retinoid",
    "salicylic acid", "benzoyl peroxide", "niacinamide",
    "hyaluronic acid", "vitamin c serum",

    # hair / scalp (often part of dermatology)
    "dandruff", "seborrheic dermatitis", "scalp", "hair loss",
    "alopecia", "hair fall",
]

def is_skin_related(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    return any(kw in t for kw in SKIN_KEYWORDS)

def extract_generic_qa(example, q_keys, a_keys, source_name):
    question = ""
    for k in q_keys:
        if k in example and example[k] is not None:
            q = str(example[k]).strip()
            if q:
                question = q
                break

    answer = ""
    for k in a_keys:
        if k in example and example[k] is not None:
            a = str(example[k]).strip()
            if a:
                answer = a
                break

    return {
        "question": question,
        "answer": answer,
        "source": source_name,
    }

print("Loading petkopetkov/medical-question-answering-all ...")
med_all = load_dataset("petkopetkov/medical-question-answering-all", split="train")

def map_med_all(ex):
    return extract_generic_qa(
        ex,
        q_keys=["question", "input", "prompt"],
        a_keys=["answer", "output", "response"],
        source_name="medical-question-answering-all",
    )

med_all_simple = med_all.map(map_med_all, remove_columns=med_all.column_names)

print("Filtering skin-related QA from medical-question-answering-all ...")
med_all_skin = med_all_simple.filter(
    lambda ex: is_skin_related(ex["question"]) or is_skin_related(ex["answer"])
)

print("Skin QA from medical-question-answering-all:", len(med_all_skin))


# ---------------------------------------------------
# 4. Dataset 2: lavita/MedQuAD (high-quality medical QA)
#    Filter to skin / dermatology questions
# ---------------------------------------------------
print("Loading lavita/MedQuAD ...")
medquad = load_dataset("lavita/MedQuAD", split="train")

def map_medquad(ex):
    return {
        "question": str(ex.get("question", "")).strip(),
        "answer": str(ex.get("answer", "")).strip(),
        "source": "MedQuAD",
    }

medquad_simple = medquad.map(map_medquad, remove_columns=medquad.column_names)

print("Filtering skin-related QA from MedQuAD ...")
medquad_skin = medquad_simple.filter(
    lambda ex: is_skin_related(ex["question"]) or is_skin_related(ex["answer"])
)

print("Skin QA from MedQuAD:", len(medquad_skin))


try:
    print("Loading Mreeb/Dermatology-Question-Answer-Dataset-For-Fine-Tuning ...")
    derm1 = load_dataset(
        "Mreeb/Dermatology-Question-Answer-Dataset-For-Fine-Tuning",
        split="train"
    )

    def map_derm1(ex):
        return extract_generic_qa(
            ex,
            q_keys=["question", "prompt", "input"],
            a_keys=["answer", "response", "output"],
            source_name="Dermatology-Question-Answer",
        )

    derm1_simple = derm1.map(map_derm1, remove_columns=derm1.column_names)

    # It's already dermatology, but filter with is_skin_related for safety
    derm1_skin = derm1_simple.filter(
        lambda ex: is_skin_related(ex["question"]) or is_skin_related(ex["answer"])
    )
    print("Skin QA from Dermatology-Question-Answer:", len(derm1_skin))

except Exception as e:
    print("Could not load Mreeb/Dermatology-Question-Answer-Dataset-For-Fine-Tuning.")
    print("Error:", e)
    derm1_skin = Dataset.from_list([])

try:
    print("Loading kingabzpro/dermatology-qa-firecrawl-dataset ...")
    derm2 = load_dataset("kingabzpro/dermatology-qa-firecrawl-dataset", split="train")

    def map_derm2(ex):
        return extract_generic_qa(
            ex,
            q_keys=["question"],
            a_keys=["answer"],
            source_name="dermatology-qa-firecrawl",
        )

    derm2_simple = derm2.map(map_derm2, remove_columns=derm2.column_names)

    # Again, already dermatology, but we keep the same filter
    derm2_skin = derm2_simple.filter(
        lambda ex: is_skin_related(ex["question"]) or is_skin_related(ex["answer"])
    )
    print("Skin QA from dermatology-qa-firecrawl:", len(derm2_skin))

except Exception as e:
    print("Could not load kingabzpro/dermatology-qa-firecrawl-dataset.")
    print("Error:", e)
    derm2_skin = Dataset.from_list([])

print("Combining datasets ...")
combined_list = list(med_all_skin) + list(medquad_skin) + list(derm1_skin) + list(derm2_skin)
combined = Dataset.from_list(combined_list)
print("Combined before dedup:", len(combined))

# Deduplicate and remove empty Q/A
seen = set()
unique_rows = []
for ex in combined:
    q = ex["question"].strip()
    a = ex["answer"].strip()
    if not q or not a:
        continue
    key = (q, a)
    if key in seen:
        continue
    seen.add(key)
    unique_rows.append(ex)

combined_unique = Dataset.from_list(unique_rows)
print("After dedup:", len(combined_unique))

# Shuffle for randomness
combined_unique = combined_unique.shuffle(seed=42)

# Select up to 5000 examples
TARGET_N = 5000
final_n = min(TARGET_N, len(combined_unique))
skin_5000 = combined_unique.select(range(final_n))

print(f"Final skin-care / dermatology QA count: {final_n}")

# ---------------------------------------------------
# 8. Save to JSONL and CSV
# ---------------------------------------------------
output_jsonl = "skincare_dermatology_med_chatbot_qa.jsonl"
output_csv = "skincare_dermatology_med_chatbot_qa.csv"

skin_5000.to_json(output_jsonl, lines=True, orient="records", force_ascii=False)
skin_5000.to_csv(output_csv, index=False)

print("Saved skin-care QA to:")
print("  -", output_jsonl)
print("  -", output_csv)
