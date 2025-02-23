import os
from collections import Counter

import matplotlib.pyplot as plt
import seaborn as sns
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import classification_report, confusion_matrix
from torch.optim.lr_scheduler import ReduceLROnPlateau

from src.model.base_models import Wav2Vec2FeatureExtractor
from src.model.model import SERBenchmarkModel
from src.utils.constant import DATASET
from src.utils.data_loader import get_dataloader
from src.utils.dataset import SpeechEmotionDataset
from src.utils.encoder import emotion_converter

# Hyperparameters
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
LEARNING_RATE = float(os.getenv("LEARNING_RATE", 0.001))
EPOCHS = int(os.getenv("EPOCHS", 5))
EARLY_STOPPING_PATIENCE = int(os.getenv("EARLY_STOPPING_PATIENCE", 5))

os.makedirs("./checkpoints", exist_ok=True)
os.makedirs("./logs", exist_ok=True)


def plot_loss(train_losses, val_losses, path: str):
    plt.figure(figsize=(10, 5))
    plt.plot(train_losses, label="Train Loss")
    plt.plot(val_losses, label="Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    parts = path.split("_",3)
    if len(parts) >= 3:
        plt.title(f"Training and Validation Loss of {parts[0]} - {parts[1]} ({parts[3]})")
    else:
        plt.title("Training and Validation Loss")
    plt.savefig(f"./logs/{path}_loss_curve.png")
    plt.close()


def plot_confusion_matrix(y_true, y_pred, classes, phase, path):

    y_true = [emotion_converter(y, mode="decode") for y in y_true]
    y_pred = [emotion_converter(y, mode="decode") for y in y_pred]

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=classes,
        yticklabels=classes,
    )
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    parts = path.split("_",3)
    if len(parts) >= 3:
        plt.title(f"{phase} Confusion Matrix of {parts[0]} - {parts[1]} ({parts[3]})")
    else:
        plt.title(f"{phase} Confusion Matrix")
    plt.savefig(f"./logs/{path}_{phase}_confusion_matrix.png")
    plt.close()


def print_classification_report(y_true, y_pred, phase, path):
    y_true = [emotion_converter(y, mode="decode") for y in y_true]
    y_pred = [emotion_converter(y, mode="decode") for y in y_pred]

    report = classification_report(
        y_true, y_pred, target_names=[str(i) for i in range(5)]
    )
    with open(f"./logs/{path}_{phase}_classification_report.txt", "w") as f:
        f.write(report)


def train(
    model, dataloaders, criterion, optimizer, scheduler, device, base_path
):

    model_path = os.path.join("./checkpoints", f"{base_path}.pth")

    best_loss = float("inf")
    patience_counter = 0
    train_losses, val_losses = [], []
    y_true_val, y_pred_val = [], []
    y_true_test, y_pred_test = [], []

    for epoch in range(EPOCHS):
        print(f"\nEpoch {epoch+1}/{EPOCHS}")

        for phase in ["train", "val", "test"]:
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

                    if phase in ["val", "test"]:
                        if phase == "val":
                            y_true_val.extend(labels.cpu().numpy())
                            y_pred_val.extend(
                                torch.argmax(outputs, dim=1).cpu().numpy()
                            )
                        else:
                            y_true_test.extend(labels.cpu().numpy())
                            y_pred_test.extend(
                                torch.argmax(outputs, dim=1).cpu().numpy()
                            )

                running_loss += loss.item() * audio.size(0)

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            print(f"{phase} Loss: {epoch_loss:.4f}")

            if phase == "train":
                train_losses.append(epoch_loss)
            else:
                if phase == "val":
                    val_losses.append(epoch_loss)
                    scheduler.step(epoch_loss)

                    if epoch_loss < best_loss:
                        best_loss = epoch_loss
                        patience_counter = 0
                        print("Saving best model...")
                        torch.save(model.state_dict(), model_path)
                    else:
                        patience_counter += 1
                        if patience_counter >= EARLY_STOPPING_PATIENCE:
                            print("Early stopping triggered!")
                            plot_loss(train_losses, val_losses, base_path)
                            plot_confusion_matrix(
                                y_true_val,
                                y_pred_val,
                                classes=[0, 1, 2, 3, 4],
                                phase="val",
                                path=base_path,
                            )
                            print_classification_report(
                                y_true_val,
                                y_pred_val,
                                phase="val",
                                path=base_path,
                            )
                            plot_confusion_matrix(
                                y_true_test,
                                y_pred_test,
                                classes=[0, 1, 2, 3, 4],
                                phase="test",
                                path=base_path,
                            )
                            print_classification_report(
                                y_true_test,
                                y_pred_test,
                                phase="test",
                                path=base_path,
                            )
                            return

    plot_loss(train_losses, val_losses, path=base_path)
    plot_confusion_matrix(
        y_true_val,
        y_pred_val,
        classes=[0, 1, 2, 3, 4],
        phase="val",
        path=base_path,
    )
    print_classification_report(
        y_true_val, y_pred_val, phase="val", path=base_path
    )
    plot_confusion_matrix(
        y_true_test,
        y_pred_test,
        classes=[0, 1, 2, 3, 4],
        phase="test",
        path=base_path,
    )
    print_classification_report(
        y_true_test, y_pred_test, phase="test", path=base_path
    )


if __name__ == "__main__":
    CUR_DATASET = DATASET.ASED

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dataset = SpeechEmotionDataset(
        dataset_name=CUR_DATASET.value.name,
        dataset_path=f"meta_csvs/{CUR_DATASET.value.language}_{CUR_DATASET.value.name}.csv",
        language=CUR_DATASET.value.language,
    )

    dataloaders = get_dataloader(
        dataset, BATCH_SIZE, shuffle=True, val_split=True
    )

    label_counts = Counter()
    for batch in dataloaders["train"]:
        labels, audio = batch["audio"], batch["labels"]
        label_counts.update(labels.tolist())

    num_of_classes = len(list(label_counts.keys()))
    en_labels = list(label_counts.keys()).sort()

    feature_extractor = Wav2Vec2FeatureExtractor(device=device)
    base_model_name = feature_extractor.model_name.replace("/","_")

    model = SERBenchmarkModel(
        feature_extractor=feature_extractor,
        num_classes=num_of_classes,
        device=device,
    ).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    scheduler = ReduceLROnPlateau(
        optimizer, mode="min", factor=0.5, patience=2
    )

    train(
        model=model,
        dataloaders=dataloaders,
        criterion=criterion,
        optimizer=optimizer,
        scheduler=scheduler,
        device=device,
        base_path=f"{CUR_DATASET.value.language}_{CUR_DATASET.value.name}_{base_model_name}",
    )
