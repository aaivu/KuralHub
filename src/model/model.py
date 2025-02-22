import librosa
import numpy as np
import torch
from torch import nn

from src.model.base_models import Wav2Vec2FeatureExtractor


class SERBenchmarkModel(nn.Module):
    def __init__(
        self,
        feature_extractor: nn.Module,
        device:str,
        hidden_dim: int = 256,
        num_classes: int = 6,
        dropout: float = 0.3,
    ):
        super(SERBenchmarkModel, self).__init__()
        self.feature_extractor = feature_extractor
        self.hidden_dim = hidden_dim
        self.dropout = dropout
        self.device = device

        self.classifier = nn.Sequential(
            nn.Linear(
                self.feature_extractor.model.config.hidden_size,
                self.hidden_dim,
            ),
            nn.ReLU(),
            nn.Dropout(self.dropout),
            nn.Linear(self.hidden_dim, num_classes),
        )

    def forward(self, audios: list[np.ndarray], sr: int = 16000) -> torch.Tensor:
        all_outputs = []
        
        for audio in audios:
            features = self.feature_extractor.extract_features(audio, sr)
            features = torch.tensor(features).unsqueeze(0)
            features = features.to(self.device)
            output = self.classifier(features[0])
            all_outputs.append(output)

        return torch.stack(all_outputs)


if __name__ == "__main__":
    feature_extractor = Wav2Vec2FeatureExtractor()

    model = SERBenchmarkModel(feature_extractor=feature_extractor)

    audio_path = "./src/tests/test_audio.wav"
    audio, sr = librosa.load(audio_path, sr=16000)

    output = model(audio)
    # Audio shape: torch.Size([32, 50000]) => Audio shape: (51542,)

    print(output)
    assert output is not None
