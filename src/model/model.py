import numpy as np
import torch
from torch import nn


class SERBenchmarkModel(nn.Module):
    def __init__(
        self,
        feature_extractor: nn.Module,
        device: str,
        num_classes: int,
        hidden_dim: int = 512,
        dropout: float = 0.3,
    ):
        super().__init__()
        self.feature_extractor = feature_extractor
        self.device = device
        self.classifier = nn.Sequential(
            nn.Linear(feature_extractor.model.config.hidden_size, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, num_classes),
        )

    def forward(self, audios: list[np.ndarray], sr: int = 16000):
        outputs = []
        for audio in audios:
            features = self.feature_extractor.extract_features(audio, sr)
            features = torch.tensor(features).unsqueeze(0).to(self.device)
            outputs.append(self.classifier(features[0]))
        return torch.stack(outputs)
