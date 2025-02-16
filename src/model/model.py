from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

import torch
from torch import nn
from transformers import AutoConfig, AutoModel


@dataclass
class SpeechModelConfig:
    """Configuration class for speech models"""

    model_name: str
    hidden_size: int = 768
    num_classes: Optional[int] = None
    dropout: float = 0.1
    hidden_dim: int = 256
    sample_rate: int = 16000
    max_length: Optional[int] = None


class BaseSpeechModel(nn.Module):
    """Base class for all speech models"""

    def __init__(self, config: SpeechModelConfig):
        super().__init__()
        self.config = config

    def preprocess_audio(self, audio: torch.Tensor) -> torch.Tensor:
        """Basic audio preprocessing"""
        if audio.dim() == 1:
            audio = audio.unsqueeze(0)
        return audio

    def postprocess_output(self, output: torch.Tensor) -> torch.Tensor:
        """Basic output postprocessing"""
        return output

    def save_model(self, path: str):
        """Save model weights and config"""
        torch.save(
            {"model_state_dict": self.state_dict(), "config": self.config},
            path,
        )

    def load_model(self, path: str):
        """Load model weights and config"""
        checkpoint = torch.load(path)
        self.load_state_dict(checkpoint["model_state_dict"])
        self.config = checkpoint["config"]


class BaseTransformerSpeechModel(BaseSpeechModel):
    """Base class for transformer-based speech models"""

    def __init__(self, config: SpeechModelConfig):
        super().__init__(config)
        self.base_model = None
        self.classifier = (
            None if config.num_classes is None else self._build_classifier()
        )

    def _build_classifier(self) -> nn.Module:
        """Build classification head"""
        return nn.Sequential(
            nn.Linear(self.config.hidden_size, self.config.hidden_dim),
            nn.ReLU(),
            nn.Dropout(self.config.dropout),
            nn.Linear(self.config.hidden_dim, self.config.num_classes),
        )

    def get_attention_mask(self, input_values: torch.Tensor) -> torch.Tensor:
        """Generate attention mask"""
        return torch.ones_like(input_values)

    def forward(self, *args, **kwargs):
        """Default forward pass"""
        raise NotImplementedError


class BaseEncoderOnlySpeechModel(BaseTransformerSpeechModel):
    """Base class for encoder-only models like HuBERT, Wav2Vec, etc."""

    def __init__(self, config: SpeechModelConfig):
        super().__init__(config)

    def extract_features(self, input_values: torch.Tensor) -> torch.Tensor:
        """Extract features from audio input"""
        outputs = self.base_model(input_values)
        return outputs.last_hidden_state

    def forward(self, input_values: torch.Tensor, **kwargs):
        """Forward pass for encoder-only models"""
        features = self.extract_features(input_values)
        pooled_output = features.mean(dim=1)
        if self.classifier is not None:
            return self.classifier(pooled_output)
        return pooled_output


class BaseEncoderDecoderSpeechModel(BaseTransformerSpeechModel):
    """Base class for encoder-decoder models like Whisper"""

    def __init__(self, config: SpeechModelConfig):
        super().__init__(config)

    def encode(self, input_values: torch.Tensor) -> torch.Tensor:
        """Encode audio input"""
        return self.base_model.encoder(input_values)

    def decode(self, encoder_outputs: torch.Tensor, **kwargs) -> torch.Tensor:
        """Decode encoded features"""
        return self.base_model.decoder(encoder_outputs, **kwargs)

    def forward(self, input_values: torch.Tensor, **kwargs):
        """Forward pass for encoder-decoder models"""
        encoder_outputs = self.encode(input_values)
        decoder_outputs = self.decode(encoder_outputs, **kwargs)
        if self.classifier is not None:
            return self.classifier(decoder_outputs.mean(dim=1))
        return decoder_outputs


class HuBERTModel(BaseEncoderOnlySpeechModel):
    def __init__(self, config: SpeechModelConfig):
        super().__init__(config)
        self.base_model = AutoModel.from_pretrained("facebook/hubert-base")


class Wav2VecModel(BaseEncoderOnlySpeechModel):
    def __init__(self, config: SpeechModelConfig):
        super().__init__(config)
        self.base_model = AutoModel.from_pretrained("facebook/wav2vec2-base")


class WhisperModel(BaseEncoderDecoderSpeechModel):
    def __init__(self, config: SpeechModelConfig):
        super().__init__(config)
        self.base_model = AutoModel.from_pretrained("openai/whisper-base")


if __name__ == "__main__":
    config = SpeechModelConfig(
        model_name="wav2vec2-base", num_classes=4, hidden_dim=256, dropout=0.1
    )

    model = Wav2VecModel(config)

    dummy_input = torch.randn(2, 16000)

    output = model(dummy_input)
    print(f"Output shape: {output.shape}")
