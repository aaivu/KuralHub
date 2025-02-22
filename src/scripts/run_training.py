import os
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from torch.optim.lr_scheduler import ReduceLROnPlateau
from sklearn.metrics import confusion_matrix

from src.model.base_models import Wav2Vec2FeatureExtractor
from src.model.model import SERBenchmarkModel
from src.utils.constant import DATASET
from src.utils.data_loader import get_dataloader
from src.utils.dataset import SpeechEmotionDataset

# Hyperparameters
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
LEARNING_RATE = float(os.getenv("LEARNING_RATE", 0.001))
EPOCHS = int(os.getenv("EPOCHS", 50))
EARLY_STOPPING_PATIENCE = int(os.getenv("EARLY_STOPPING_PATIENCE", 5))
CHECKPOINT_PATH = os.getenv("CHECKPOINT_PATH", "./checkpoints/model.pth")

# Create necessary directories
os.makedirs("./checkpoints", exist_ok=True)
os.makedirs("./logs", exist_ok=True)

def plot_loss(train_losses, val_losses):
    plt.figure(figsize=(10, 5))
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.title("Training and Validation Loss")
    plt.savefig("./logs/loss_curve.png")
    plt.close()

def plot_confusion_matrix(y_true, y_pred, classes):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title("Confusion Matrix")
    plt.savefig("./logs/confusion_matrix.png")
    plt.close()

def train(model, dataloaders, criterion, optimizer, scheduler, device):
    best_loss = float("inf")
    patience_counter = 0
    train_losses, val_losses = [], []
    y_true, y_pred = [], []

    for epoch in range(EPOCHS):
        print(f"\nEpoch {epoch+1}/{EPOCHS}")
        
        for phase in ["train", "val"]:
            if phase not in dataloaders:
                continue
            
            model.train() if phase == "train" else model.eval()
            running_loss = 0.0
            
            for batch in dataloaders[phase]:
                labels, audio = batch["audio"], batch["labels"]
                audio, labels = audio.to(device), labels.to(device)
                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == "train"):
                    outputs = model(audio)
                    labels = labels.long()
                    loss = criterion(outputs.float(), labels)
                    
                    if phase == "train":
                        loss.backward()
                        optimizer.step()
                    
                    if phase == "val":
                        y_true.extend(labels.cpu().numpy())
                        y_pred.extend(torch.argmax(outputs, dim=1).cpu().numpy())
                
                running_loss += loss.item() * audio.size(0)
            
            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            print(f"{phase} Loss: {epoch_loss:.4f}")
            
            if phase == "train":
                train_losses.append(epoch_loss)
            else:
                val_losses.append(epoch_loss)
                scheduler.step(epoch_loss)
                
                if epoch_loss < best_loss:
                    best_loss = epoch_loss
                    patience_counter = 0
                    print("Saving best model...")
                    torch.save(model.state_dict(), CHECKPOINT_PATH)
                else:
                    patience_counter += 1
                    if patience_counter >= EARLY_STOPPING_PATIENCE:
                        print("Early stopping triggered!")
                        plot_loss(train_losses, val_losses)
                        plot_confusion_matrix(y_true, y_pred, classes=[0, 1, 2, 3, 4])
                        return
    
    plot_loss(train_losses, val_losses)
    plot_confusion_matrix(y_true, y_pred, classes=[0, 1, 2, 3, 4])

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dataset = SpeechEmotionDataset(
        dataset_name=DATASET.EMOTA.value.name,
        dataset_path=f"meta_csvs/{DATASET.EMOTA.value.language}_{DATASET.EMOTA.value.name}.csv",
        language=DATASET.EMOTA.value.language,
    )
    
    dataloaders = get_dataloader(dataset, BATCH_SIZE, shuffle=True, val_split=True)

    feature_extractor = Wav2Vec2FeatureExtractor(device=device)
    
    model = SERBenchmarkModel(feature_extractor=feature_extractor, num_classes=5, device=device).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    scheduler = ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=2)
    
    train(model, dataloaders, criterion, optimizer, scheduler, device)