import os

import librosa
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

from src.utils.encoder import emotion_converter
from src.utils.utils import get_logger, is_valid_wav

logger = get_logger(__name__)


def pad_or_truncate(audio, desired_length=30000):
    if len(audio) >= desired_length:
        return audio[:desired_length]
    return np.pad(audio, (0, desired_length - len(audio)), mode="constant")


class SpeechEmotionDataset(Dataset):
    def __init__(
        self,
        dataset_name: str,
        dataset_path: str,
        language: str,
        sr: int = 16000,
    ) -> None:
        self.dataset_name = dataset_name
        self.language = language

        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Metadata file not found: {dataset_path}")
        self.dataset = pd.read_csv(dataset_path)
        if "emotion" not in self.dataset.columns:
            raise ValueError("Metadata file must contain an 'emotion' column.")

        self.available_emotions = sorted(self.dataset["emotion"].unique())
        self.EMOTION_MAPPING = {
            emotion: idx for idx, emotion in enumerate(self.available_emotions)
        }

        self.audios, emotions = [], []
        for path, emotion in zip(
            self.dataset["audio_path"].astype(str), self.dataset["emotion"]
        ):
            if not is_valid_wav(path):
                logger.warning(f"Skipping invalid file: {path}")
                continue
            audio, _ = librosa.load(path, sr=sr)
            self.audios.append(pad_or_truncate(audio, 50000))
            emotions.append(
                emotion_converter(emotion, self.EMOTION_MAPPING)[0]
            )
        self.emotions = torch.tensor(emotions, dtype=torch.long)

    def __len__(self) -> int:
        return len(self.emotions)

    def __getitem__(self, idx: int) -> dict:
        return {"audio": self.audios[idx], "labels": self.emotions[idx]}
