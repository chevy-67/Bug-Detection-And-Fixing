import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load the fine-tuned model and tokenizer
model_path = "d:/BUG FIXER API/bug_fixing_app/saved_model"  # Update with your actual path
model = T5ForConditionalGeneration.from_pretrained(model_path)
tokenizer = T5Tokenizer.from_pretrained(model_path)

# Set the model to evaluation mode
model.eval()

def fix_code(buggy_code):
    """
    Given a buggy code snippet, this function uses the fine-tuned T5 model
    to generate a fixed version of the code.
    """
    # Prepare input for the model
    input_text = f"fix: {buggy_code.strip()}"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    # Generate the fix
    with torch.no_grad():
        output_ids = model.generate(input_ids, max_length=200)

    # Decode and return the fixed code
    fixed_code = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return fixed_code

if __name__ == "__main__":
    # Example buggy code snippet
    buggy_code = """
def divide(a, b):
    return a / b  # Potential division by zero bug
"""

    # Run the model to fix the bug
    fixed_code = fix_code(buggy_code)

    # Print the results
    print("==== Buggy Code ====")
    print(buggy_code)
    print("\n==== Fixed Code ====")
    print(fixed_code)
