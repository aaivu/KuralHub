import torch
from transformers import AutoTokenizer


class SERPredictor:
    def __init__(self, model, tokenizer_name, device="cpu"):
        self.model = model.to(device)
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.device = device

    def predict(self, text):
        inputs = self.tokenizer(
            text, return_tensors="pt", padding=True, truncation=True
        )
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)

        with torch.no_grad():
            logits = self.model(input_ids, attention_mask)

        probs = torch.softmax(logits, dim=-1)

        predicted_class = torch.argmax(probs, dim=-1).item()

        return predicted_class, probs.cpu().numpy()
