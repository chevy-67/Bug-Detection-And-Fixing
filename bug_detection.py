from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Load pre-trained CodeBERT model
model_name = "microsoft/codebert-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)  # 2 labels: Buggy or Not

# Function to predict if code is buggy
def detect_bug(code_snippet):
    inputs = tokenizer(code_snippet, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=-1).item()

    return "Buggy" if prediction == 1 else "Not Buggy"

# Example usage
sample_code = 'runtimeService.startProcessInstanceByKey("shellCommandStart");'
print("Prediction:", detect_bug(sample_code))
