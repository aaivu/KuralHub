import numpy as np
import torch
import torch.nn as nn
from transformers import (
    AutoFeatureExtractor,
    AutoModel,
    HubertModel,
    Wav2Vec2Model,
    Wav2Vec2Processor,
    WavLMModel,
    WhisperModel,
    WhisperProcessor,
)

from src.utils.constant import BASE_MODEL


class BaseFeatureExtractor(nn.Module):
    processor_cls = AutoFeatureExtractor
    model_cls = AutoModel

    def __init__(self, model_name: str, device: str = None):
        super().__init__()
        self.device = device or (
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.processor = self.processor_cls.from_pretrained(model_name)
        self.model = self.model_cls.from_pretrained(model_name).to(self.device)
        self.model.eval()
        self.model_name = model_name

    def extract_features(self, audio: np.ndarray, sr: int = 16000):
        if isinstance(audio, torch.Tensor):
            audio = audio.detach().cpu().numpy()
        inputs = self.processor(audio, sampling_rate=sr, return_tensors="pt")
        is_whisper = isinstance(self.model, WhisperModel)
        values = (
            inputs.input_features if is_whisper else inputs.input_values
        ).to(self.device)
        with torch.no_grad():
            encoder = self.model.encoder if is_whisper else self.model
            hidden = encoder(values, output_hidden_states=True)
        return hidden.last_hidden_state.mean(dim=1).cpu().numpy().squeeze()


class WhisperFeatureExtractor(BaseFeatureExtractor):
    processor_cls, model_cls = WhisperProcessor, WhisperModel


class WavLMFeatureExtractor(BaseFeatureExtractor):
    model_cls = WavLMModel


class Wav2Vec2FeatureExtractor(BaseFeatureExtractor):
    processor_cls, model_cls = Wav2Vec2Processor, Wav2Vec2Model


class HuBERTFeatureExtractor(BaseFeatureExtractor):
    model_cls = HubertModel


class Wav2Vec2XLRFeatureExtractor(BaseFeatureExtractor):
    pass


class FeatureExtractorFactory:
    extractors = {
        BASE_MODEL.WAV2VEC2_BASE.value: Wav2Vec2FeatureExtractor,
        BASE_MODEL.WAV2VEC2_LARGE_LV60.value: Wav2Vec2FeatureExtractor,
        BASE_MODEL.WAV2VEC2_LARGE_960H.value: Wav2Vec2FeatureExtractor,
        BASE_MODEL.XLS_R_300M.value: Wav2Vec2XLRFeatureExtractor,
        BASE_MODEL.XLS_R_1B.value: Wav2Vec2XLRFeatureExtractor,
        BASE_MODEL.HUBERT_BASE.value: HuBERTFeatureExtractor,
        BASE_MODEL.HUBERT_LARGE_LS960.value: HuBERTFeatureExtractor,
        BASE_MODEL.WAVLM_BASE_PLUS.value: WavLMFeatureExtractor,
        BASE_MODEL.WAVLM_LARGE.value: WavLMFeatureExtractor,
        BASE_MODEL.OPENAI_WHISPER_SMALL.value: WhisperFeatureExtractor,
        BASE_MODEL.OPENAI_WHISPER_LARGE.value: WhisperFeatureExtractor,
    }

    @staticmethod
    def get_extractor(model_name: str, device: str = None):
        if model_name not in FeatureExtractorFactory.extractors:
            raise ValueError(f"Unsupported model: {model_name}")
        return FeatureExtractorFactory.extractors[model_name](
            model_name, device
        )
