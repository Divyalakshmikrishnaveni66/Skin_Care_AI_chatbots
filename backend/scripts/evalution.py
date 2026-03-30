# ----------EVALUATION-----------------
#6. you can directly load it from Drive:
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Correct path to the finetuned model
finetuned_path = "/content/drive/MyDrive/MyFinetunedModel"

tokenizer = AutoTokenizer.from_pretrained(finetuned_path)
model = AutoModelForSeq2SeqLM.from_pretrained(finetuned_path)

def answer_question(question):
    # Adjust the prompt for a QA chatbot
    prompt = f"question: {question} answer:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100) # Increased max_new_tokens for potentially longer answers
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Test with some relevant questions
print(answer_question("What is acne?"))
print(answer_question("How to treat eczema?"))
