import numpy as np
import pytest
import torch

from src.model.base_models import FeatureExtractorFactory
from src.model.model import SERBenchmarkModel
from src.utils.constant import BASE_MODEL
from src.utils.data_loader import get_dataloader
from src.utils.dataset import pad_or_truncate
from src.utils.encoder import emotion_converter
from src.utils.utils import stratified_sampling

MAPPING = {"ANGER": 0, "FEAR": 1, "NEUTRAL": 2}


class FakeExtractor(torch.nn.Module):
    class model:
        class config:
            hidden_size = 8

    def extract_features(self, audio, sr):
        return np.full(8, float(len(audio)), dtype=np.float32)


def test_emotion_converter_round_trip():
    idx, _ = emotion_converter("FEAR", MAPPING)
    assert idx == 1
    assert emotion_converter(idx, MAPPING, mode="decode") == "FEAR"
    with pytest.raises(ValueError):
        emotion_converter("JOY", MAPPING)


def test_pad_or_truncate():
    assert len(pad_or_truncate(np.ones(10), 25)) == 25
    assert len(pad_or_truncate(np.ones(40), 25)) == 25


def test_dataloader_splits_cover_dataset():
    loaders = get_dataloader(list(range(100)), 8, True, val_split=True)
    sizes = {k: len(v.dataset) for k, v in loaders.items()}
    assert sizes == {"train": 80, "val": 10, "test": 10}


def test_stratified_sampling_caps_size():
    data = [["ANGER", f"a{i}"] for i in range(30)]
    data += [["FEAR", f"f{i}"] for i in range(30)]
    assert len(stratified_sampling(data, 20)) == 20
    assert stratified_sampling(data[:5], 20) == data[:5]


def test_classification_head_shape():
    model = SERBenchmarkModel(FakeExtractor(), device="cpu", num_classes=3)
    out = model([np.zeros(100), np.zeros(200)])
    assert out.shape == (2, 3)


@pytest.mark.local_only
@pytest.mark.parametrize("name", [m.value for m in BASE_MODEL])
def test_feature_extractor_output(name):
    extractor = FeatureExtractorFactory.get_extractor(name, device="cpu")
    features = extractor.extract_features(np.zeros(16000, dtype=np.float32))
    assert features.shape == (extractor.model.config.hidden_size,)
