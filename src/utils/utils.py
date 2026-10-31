import logging
import os

import pandas as pd
import soundfile as sf
from sklearn.model_selection import StratifiedShuffleSplit


def get_logger(name: str = __name__, level: int = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
        logger.addHandler(handler)
    return logger


def get_wav_files(root_dir, extention=".wav"):
    return [
        os.path.join(dirpath, f)
        for dirpath, _, files in os.walk(root_dir)
        for f in files
        if f.endswith(extention)
    ]


def is_valid_wav(file_path):
    try:
        with sf.SoundFile(file_path):
            return True
    except RuntimeError:
        return False


def stratified_sampling(data, max_files):
    if len(data) <= max_files:
        return data
    df = pd.DataFrame(data, columns=["emotion", "path"])
    splitter = StratifiedShuffleSplit(
        n_splits=1, train_size=max_files, random_state=42
    )
    train_idx, _ = next(splitter.split(df, df["emotion"]))
    return df.iloc[train_idx].values.tolist()
