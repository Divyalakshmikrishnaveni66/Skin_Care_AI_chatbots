# ======================= 0. IMPORT =======================
import os
import json
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model

# ======================= 1. CONFIG =======================
model_type = "flan"
hf_model_id = "google/flan-t5-base"

# Windows paths
model_dir = "C:/Users/vsure/OneDrive/Desktop/skin_care/models/flan_t5_base"
data_path = "C:/Users/vsure/OneDrive/Desktop/skin_care/skincare_dermatology_med_chatbot_qa.jsonl"
output_dir = "C:/Users/vsure/OneDrive/Desktop/skin_care/MyFinetunedModel"

os.makedirs(model_dir, exist_ok=True)  
os.makedirs(output_dir, exist_ok=True)


# ======================= 2. LOAD MODEL ====================
if not os.path.exists(os.path.join(model_dir, "config.json")):
    print("⬇️ Model not found → Downloading from Hugging Face...")
    tokenizer = AutoTokenizer.from_pretrained(hf_model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(hf_model_id)
    tokenizer.save_pretrained(model_dir)
    model.save_pretrained(model_dir)
    print("✅ Model downloaded & saved")
else:
    print("✅ Model found locally → Loading")
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# ======================= 3. LOAD DATA =====================
print("\n📂 Loading dataset...")
data = []
if data_path.endswith(".jsonl"):
    with open(data_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
else:
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
print(f"✅ Loaded {len(data):,} examples")

# ======================= 4. FORMAT DATA ===================
def format_example(x):
    if isinstance(x, dict):
        if "source" in x and "target" in x:
            return {"input_text": x["source"], "target_text": x["target"]}
        if "question" in x and "answer" in x:
            return {"input_text": x["question"], "target_text": x["answer"]}
        if "text" in x:
            return {"input_text": x["text"], "target_text": x["text"]}
    return {"input_text": str(x), "target_text": str(x)}

dataset = Dataset.from_list([format_example(x) for x in data])

# ======================= 5. TOKENIZATION ==================
def tokenize(ex):
    inp = tokenizer(ex["input_text"], truncation=True, padding="max_length", max_length=256)
    lab = tokenizer(ex["target_text"], truncation=True, padding="max_length", max_length=256)
    inp["labels"] = lab["input_ids"]
    return inp

tokenized = dataset.map(tokenize, batched=True, remove_columns=dataset.column_names)

# ======================= 6. APPLY LoRA ====================
lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    target_modules=["q", "v"],
    lora_dropout=0.05,
    bias="none",
    task_type="SEQ_2_SEQ_LM"
)
model = get_peft_model(model, lora_config)

# ======================= 7. TRAIN ========================
training_args = TrainingArguments(
    output_dir=output_dir,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    logging_steps=20,
    save_steps=500,
    save_total_limit=2,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    tokenizer=tokenizer
)

print("\n🚀 Training Started...\n")
trainer.train()

# ======================= 8. SAVE MODEL ===================
trainer.save_model(output_dir)
tokenizer.save_pretrained(output_dir)
print("\n✅✅✅ FINETUNING COMPLETE ✅✅✅")
print("📦 Final model saved at:", output_dir)
