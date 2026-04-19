from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

model.save_pretrained("./flan_t5_base")
tokenizer.save_pretrained("./flan_t5_base")

print("✅ Model downloaded successfully!")