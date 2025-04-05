import torch
from torch.utils.data import DataLoader, Dataset
from transformers import T5ForConditionalGeneration, T5Tokenizer
from torch.cuda.amp import autocast, GradScaler

# Use a smaller model to reduce memory usage
MODEL_NAME = "t5-small"  # Changed from "t5-base"

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model and tokenizer
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME).to(device)

# Sample data
data = [
    {
        "before": 'submittedNode.get("values") != null',
        "after": 'submittedNode.get("values") == null'
    },
    {
        "before": 'Arrays.asList("ls","pwd")',
        "after": 'Arrays.asList("cmd","ls","pwd")'
    }
]

# Create a custom dataset
class BugFixDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=512):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        source_text = f"Fix this bug: {self.data[idx]['before']}"
        target_text = self.data[idx]['after']

        source = self.tokenizer(
            source_text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        target = self.tokenizer(
            target_text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        return {
            "input_ids": source["input_ids"].squeeze(0),
            "attention_mask": source["attention_mask"].squeeze(0),
            "labels": target["input_ids"].squeeze(0)
        }

# Create dataset and dataloader
batch_size = 2  # Reduced batch size
dataset = BugFixDataset(data, tokenizer)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Set optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

# Gradient accumulation to handle small batch sizes
gradient_accumulation_steps = 4
scaler = GradScaler()  # Mixed precision training

# Training loop
num_epochs = 3
for epoch in range(num_epochs):
    model.train()
    total_loss = 0

    for step, batch in enumerate(dataloader):
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        with autocast():  # Mixed precision for memory efficiency
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss / gradient_accumulation_steps  # Scale loss for accumulation

        scaler.scale(loss).backward()

        if (step + 1) % gradient_accumulation_steps == 0:
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}: Loss = {total_loss / len(dataloader)}")

# Clear memory after training
torch.cuda.empty_cache()
print("Training Complete!")
