from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_NAME = "Salesforce/codet5-base"  # Change this if using another model
SAVE_DIR = r"D:\BUG_FIXER_API\bug_fixing_app\saved_model"

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model.save_pretrained(SAVE_DIR)
tokenizer.save_pretrained(SAVE_DIR)

print(f"Model saved successfully in {SAVE_DIR}")
