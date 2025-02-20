import librosa
import numpy as np
import torch
from torch import nn

from src.model.base_models import Wav2Vec2FeatureExtractor


class SERBenchmarkModel(nn.Module):
    def __init__(
        self,
        feature_extractor: nn.Module,
        hidden_dim: int = 256,
        num_classes: int = 6,
        dropout: float = 0.3,
    ):
        super(SERBenchmarkModel, self).__init__()
        self.feature_extractor = feature_extractor
        self.hidden_dim = hidden_dim
        self.dropout = dropout

        self.classifier = nn.Sequential(
            nn.Linear(
                self.feature_extractor.model.config.hidden_size,
                self.hidden_dim,
            ),
            nn.ReLU(),
            nn.Dropout(self.dropout),
            nn.Linear(self.hidden_dim, 32),
        )

    def forward(self, audio: np.ndarray, sr: int = 16000) -> torch.Tensor:
        features = self.feature_extractor.extract_features(audio, sr)
        features = torch.tensor(features).unsqueeze(0)
        output = self.classifier(features)
        return output


if __name__ == "__main__":
    feature_extractor = Wav2Vec2FeatureExtractor()

    model = SERBenchmarkModel(feature_extractor=feature_extractor)

    audio_path = "./src/tests/test_audio.wav"
    audio, sr = librosa.load(audio_path, sr=16000)

    output = model(audio)
    # Audio shape: torch.Size([32, 50000]) => Audio shape: (51542,)

    print(output)
    assert output is not None
