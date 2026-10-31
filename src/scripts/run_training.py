import json
import os
import random
import warnings

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import classification_report, confusion_matrix
from torch.optim.lr_scheduler import ReduceLROnPlateau

from src.model.base_models import FeatureExtractorFactory
from src.model.model import SERBenchmarkModel
from src.utils.constant import BASE_MODEL, DATASET
from src.utils.data_loader import get_dataloader
from src.utils.dataset import SpeechEmotionDataset
from src.utils.encoder import emotion_converter
from src.utils.utils import get_logger

warnings.filterwarnings("ignore")
logger = get_logger(__name__)

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
os.environ["PYTHONHASHSEED"] = str(SEED)

BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
LEARNING_RATE = float(os.getenv("LEARNING_RATE", 0.001))
EPOCHS = int(os.getenv("EPOCHS", 30))
EARLY_STOPPING_PATIENCE = int(os.getenv("EARLY_STOPPING_PATIENCE", 5))
CUR_DATASET = DATASET[os.getenv("DATASET", "KAZAKHEMOTIONALTTS")]
CUR_BASE_MODEL = BASE_MODEL[os.getenv("BASE_MODEL", "XLS_R_1B")].value

MODELS_DIR = "./finetuned_models"
LOGS_DIR = "./results/train_val_test_logs"


def title(prefix, path):
    parts = path.split("_", 3)
    if len(parts) >= 3:
        return f"{prefix} of {parts[0]} - {parts[1]} ({parts[2]})"
    return prefix


def decode(ys, mapping):
    return [emotion_converter(y, mapping, mode="decode") for y in ys]


def plot_loss(train_losses, val_losses, path):
    plt.figure(figsize=(10, 5))
    plt.plot(train_losses, label="Train Loss")
    plt.plot(val_losses, label="Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.title(title("Training and Validation Loss", path))
    plt.savefig(f"{LOGS_DIR}/{path}/{path}_loss_curve.png")
    plt.close()


def save_report(y_true, y_pred, phase, path, classes, mapping):
    y_true, y_pred = decode(y_true, mapping), decode(y_pred, mapping)
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        confusion_matrix(y_true, y_pred),
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=classes,
        yticklabels=classes,
    )
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title(title(f"{phase} Confusion Matrix", path))
    plt.savefig(f"{LOGS_DIR}/{path}/{path}_{phase}_confusion_matrix.png")
    plt.close()
    with open(
        f"{LOGS_DIR}/{path}/{path}_{phase}_classification_report.txt", "w"
    ) as f:
        f.write(classification_report(y_true, y_pred))


def train(
    model,
    dataloaders,
    criterion,
    optimizer,
    scheduler,
    device,
    base_path,
    ac_labels,
    EMOTION_MAPPING,
):
    logger.info("Finetuning Started...")
    os.makedirs(f"{MODELS_DIR}/{base_path}", exist_ok=True)
    os.makedirs(f"{LOGS_DIR}/{base_path}", exist_ok=True)
    with open(f"{MODELS_DIR}/{base_path}/{base_path}.json", "w") as f:
        json.dump(EMOTION_MAPPING, f)

    best_loss, patience_counter = float("inf"), 0
    train_losses, val_losses = [], []
    y_true = {"val": [], "test": []}
    y_pred = {"val": [], "test": []}

    def save_logs():
        plot_loss(train_losses, val_losses, base_path)
        for phase in ("val", "test"):
            save_report(
                y_true[phase],
                y_pred[phase],
                phase,
                base_path,
                ac_labels,
                EMOTION_MAPPING,
            )
        logger.info("Logs Saved...")

    for epoch in range(EPOCHS):
        logger.info(f"Epoch {epoch + 1}/{EPOCHS}")
        for phase in ("train", "val", "test"):
            if phase not in dataloaders:
                continue
            model.train() if phase == "train" else model.eval()
            running_loss = 0.0

            for batch in dataloaders[phase]:
                audio = batch["audio"].to(device)
                labels = batch["labels"].to(device).long()
                optimizer.zero_grad()
                with torch.set_grad_enabled(phase == "train"):
                    outputs = model(audio)
                    loss = criterion(outputs.float(), labels)
                    if phase == "train":
                        loss.backward()
                        optimizer.step()
                    else:
                        y_true[phase].extend(labels.cpu().numpy())
                        y_pred[phase].extend(
                            torch.argmax(outputs, dim=1).cpu().numpy()
                        )
                running_loss += loss.item() * audio.size(0)

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            logger.info(f"{phase} Loss: {epoch_loss:.4f}")

            if phase == "train":
                train_losses.append(epoch_loss)
            elif phase == "val":
                val_losses.append(epoch_loss)
                scheduler.step(epoch_loss)
                if epoch_loss < best_loss:
                    best_loss, patience_counter = epoch_loss, 0
                else:
                    patience_counter += 1
                    if patience_counter >= EARLY_STOPPING_PATIENCE:
                        logger.info("Early stopping triggered!")
                        save_logs()
                        return

    logger.info("Finetuning Ended...")
    save_logs()


if __name__ == "__main__":
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    logger.info(f"Device: {device}")
    logger.info(
        f"Start finetuning {CUR_BASE_MODEL} with {CUR_DATASET.value.name}"
    )
    feature_extractor = FeatureExtractorFactory.get_extractor(
        model_name=CUR_BASE_MODEL, device=device
    )
    ds = CUR_DATASET.value
    dataset = SpeechEmotionDataset(
        dataset_name=ds.name,
        dataset_path=f"meta_csvs/{ds.language}_{ds.name}.csv",
        language=ds.language,
    )
    logger.info(f"Emotion Map is Ready: {dataset.EMOTION_MAPPING}")

    model = SERBenchmarkModel(
        feature_extractor=feature_extractor,
        num_classes=len(dataset.EMOTION_MAPPING),
        device=device,
    ).to(device)
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    train(
        model=model,
        dataloaders=get_dataloader(
            dataset, BATCH_SIZE, shuffle=True, val_split=True
        ),
        criterion=nn.CrossEntropyLoss(),
        optimizer=optimizer,
        scheduler=ReduceLROnPlateau(
            optimizer, mode="min", factor=0.5, patience=2
        ),
        device=device,
        base_path=(
            f"{ds.language}_{ds.name}_"
            f"{feature_extractor.model_name.split('/')[1]}"
        ),
        ac_labels=dataset.EMOTION_MAPPING.keys(),
        EMOTION_MAPPING=dataset.EMOTION_MAPPING,
    )
