import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import os

# Correct model path
MODEL_PATH = os.path.abspath(r"D:\BUG_FIXER_API\bug_fixing_app\saved_model")

# Load tokenizer & model
try:
    tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH, local_files_only=True)
    model.eval()
except Exception as e:
    print(f"Error loading model/tokenizer: {e}")
    exit()

# Function to fix buggy code
def generate_fix(buggy_code):
    input_text = f"Fix the following Python code:\n{buggy_code}\nCorrected version:"

    input_ids = tokenizer.encode(input_text, return_tensors="pt", truncation=True, max_length=128)

    with torch.no_grad():
        output_ids = model.generate(
            input_ids, 
            max_length=150, 
            num_beams=10,  # Better search
            num_return_sequences=1,
            early_stopping=True
        )

    fixed_code = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return fixed_code.strip()

# Test the function
if __name__ == "__main__":
    test_code = "for i in range(5) print(i)"  # Example buggy code

    print("Buggy Code:")
    print(test_code)

    fixed_code = generate_fix(test_code)

    print("\nFixed Code:")
    print(fixed_code)
