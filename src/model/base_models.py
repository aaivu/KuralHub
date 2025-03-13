import numpy as np
import torch
import torch.nn as nn
from transformers import (AutoFeatureExtractor, AutoModel, HubertModel,
                          Wav2Vec2Model, Wav2Vec2Processor, WavLMModel,
                          WhisperModel, WhisperProcessor)


class BaseFeatureExtractor(nn.Module):
    def __init__(self, model_name: str, processor, model, device: str = None):
        super(BaseFeatureExtractor, self).__init__()
        self.device = (
            device
            if device
            else ("cuda" if torch.cuda.is_available() else "cpu")
        )
        self.processor = processor.from_pretrained(model_name)
        self.model = model.from_pretrained(model_name).to(self.device)
        self.model.eval()
        self.model_name = model_name

    def extract_features(
        self, audio: np.ndarray, sr: int = 16000
    ) -> np.ndarray:
        """
        Extract features from the model.
        """
        if isinstance(audio, torch.Tensor):
            audio = audio.detach().cpu().numpy()
        if isinstance(self.model, WhisperModel):
            input_values = self.processor(
                audio, sampling_rate=sr, return_tensors="pt"
            ).input_features.to(self.device)
        else:
            input_values = self.processor(
                audio, sampling_rate=sr, return_tensors="pt"
            ).input_values.to(self.device)

        with torch.no_grad():
            if isinstance(self.model, WhisperModel):
                outputs = self.model.encoder(
                    input_values, output_hidden_states=True
                )
            else:
                outputs = self.model(input_values, output_hidden_states=True)
        last_hidden_states = outputs.last_hidden_state

        # Apply Mean Pooling
        return torch.mean(last_hidden_states, dim=1).cpu().numpy().squeeze()


class WhisperFeatureExtractor(BaseFeatureExtractor):
    def __init__(
        self, model_name: str = "openai/whisper-small", device: str = None
    ):
        processor = WhisperProcessor
        model = WhisperModel
        super().__init__(model_name, processor, model, device)


class WavLMFeatureExtractor(BaseFeatureExtractor):
    def __init__(
        self, model_name: str = "microsoft/wavlm-base-plus", device: str = None
    ):
        processor = AutoFeatureExtractor
        model = WavLMModel
        super().__init__(model_name, processor, model, device)


class Wav2Vec2FeatureExtractor(BaseFeatureExtractor):
    def __init__(
        self, model_name: str = "facebook/wav2vec2-base", device: str = None
    ):
        processor = Wav2Vec2Processor
        model = Wav2Vec2Model
        super().__init__(model_name, processor, model, device)


class HuBERTFeatureExtractor(BaseFeatureExtractor):
    def __init__(
        self,
        model_name: str = "facebook/hubert-base-ls960",
        device: str = None,
    ):
        processor = AutoFeatureExtractor
        model = HubertModel
        super().__init__(model_name, processor, model, device)


class Wav2Vec2XLRFeatureExtractor(BaseFeatureExtractor):
    def __init__(
        self,
        model_name: str = "facebook/wav2vec2-xls-r-300m",
        device: str = None,
    ):
        processor = AutoFeatureExtractor
        model = AutoModel
        super().__init__(model_name, processor, model, device)
