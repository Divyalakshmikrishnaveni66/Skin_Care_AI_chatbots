import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Official model name
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Where to save forever in your Drive
save_directory = "/content/drive/MyDrive/TinyLlama-1.1B-Chat"

os.makedirs(save_directory, exist_ok=True)

print("Downloading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

print("Downloading TinyLlama 1.1B model (~1.5 GB total)...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="cpu",              # Works perfectly on CPU
    torch_dtype=torch.float16,     # Saves RAM
    low_cpu_mem_usage=True,
    trust_remote_code=False
)

# Save to Drive (so you never download again)
print(f"Saving model + tokenizer to {save_directory}...")
tokenizer.save_pretrained(save_directory)
model.save_pretrained(save_directory)

print("SUCCESS! TinyLlama 1.1B Chat is now saved in your Drive")
print(f"Location: {save_directory}")
print("Size: ~1.5 GB | Loads in 3 seconds on CPU | Perfect for fast fine-tuning & inference")
