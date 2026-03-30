import json

INPUT_FILE = "/content/skincare_dermatology_med_chatbot_qa.jsonl"       # your input file
OUTPUT_FILE = "/content/converted.jsonl"

for line in open(INPUT_FILE, "r", encoding="utf-8"):
    line = line.strip()
    if not line:
        continue

    obj = json.loads(line)

    # Detect best possible source field
    source = (
        obj.get("input") or
        obj.get("instruction") or
        obj.get("question") or
        obj.get("context") or
        obj.get("source") or
        obj.get("prompt") or
        obj.get("text") or
        ""
    )

    # Detect best possible target field
    target = (
        obj.get("target") or
        obj.get("answer") or
        obj.get("output") or
        obj.get("response") or
        obj.get("completion") or
        ""
    )

    out = {
        "source": str(source).strip(),
        "target": str(target).strip()
    }

    with open(OUTPUT_FILE, "a", encoding="utf-8") as fout:
        fout.write(json.dumps(out, ensure_ascii=False) + "\n")

print("✅ Conversion complete!")
print("📄 Saved to:", OUTPUT_FILE)
