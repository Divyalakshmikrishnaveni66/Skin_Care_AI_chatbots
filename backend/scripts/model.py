from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Choose your model
model_name = "google/flan-t5-base"

# Path in Google Drive
save_path = "/content/drive/MyDrive/flan_t5_base"

print("Downloading model...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

print("Saving to Google Drive...")

tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)

print("DONE! Model saved at:", save_path)
