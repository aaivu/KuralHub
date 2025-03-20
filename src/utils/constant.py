from enum import Enum


class EMOTION(Enum):
    FEAR = "FEAR"
    SADNESS = "SADNESS"
    HAPPINESS = "HAPPINESS"
    ANGER = "ANGER"
    NEUTRAL = "NEUTRAL"
    DISGUST = "DISGUST"
    SURPRISE = "SURPRISE"
    CALM = "CALM"
    BOREDOM = "BOREDOM"
    SARCASTIC = "SARCASTIC"
    JOY = "JOY"


SELECTED_EMOTIONS = [
    EMOTION.ANGER.value,
    EMOTION.FEAR.value,
    EMOTION.HAPPINESS.value,
    EMOTION.SADNESS.value,
    EMOTION.NEUTRAL.value,
]


class LANGUAGE(Enum):
    ENGLISH = "en"
    GERMAN = "de"
    CHINESE = "zh"
    SPANISH = "es"
    ITALIAN = "it"
    URDU = "ur"
    TAMIL = "ta"
    TELUGU = "te"
    MALAYALAM = "ml"
    KANNADA = "kn"
    BENGALI = "bn"
    HINDI = "hi"
    FRENCH = "fr"
    AMHARIC = "am"
    PERSIAN = "fa"  # Farsi
    SWAHILI = "sw"
    KOREAN = "ko"


class Dataset:
    name: str
    language: str
    path: str
    url: str

    def __init__(self, name, language, path, url):
        self.name = name
        self.language = language
        self.path = path
        self.url = url


class DATASET(Enum):
    ASED = Dataset(
        name="ASED",
        language=LANGUAGE.AMHARIC.value,
        url="thanikansivatheepan/amharic-speech-emotional-dataset-ased",
        path="ser_datasets/ASED",
    )
    BANSPEMO = Dataset(
        name="BANSpEmo",
        language=LANGUAGE.BENGALI.value,
        url="thanikansivatheepan/bangla-lang-ser-dataset",
        path="ser_datasets/BANSpEmo/BANSpEmo Dataset",
    )
    CAFE = Dataset(
        name="CaFE",
        language=LANGUAGE.FRENCH.value,
        url="jubeerathan/cafe-dataset",
        path="ser_datasets/CaFE",
    )
    EMODB = Dataset(
        name="EmoDB",
        language=LANGUAGE.GERMAN.value,
        url="piyushagni5/berlin-database-of-emotional-speech-emodb",
        path="ser_datasets/EmoDB/wav",
    )
    EMOTA = Dataset(
        name="EmoTa",
        language=LANGUAGE.TAMIL.value,
        url="luxluxshan/tamserdb",
        path="ser_datasets/EmoTa",
    )
    EMOVO = Dataset(
        name="EMOVO",
        language=LANGUAGE.ITALIAN.value,
        url="sourabhy/emovo-italian-ser-dataset",
        path="ser_datasets/EMOVO/EMOVO",
    )
    ESD_CHINESE = Dataset(
        name="ESD",
        language=LANGUAGE.CHINESE.value,
        url="thanikansivatheepan/esd-dataset-fyp",
        path="ser_datasets/ESD/Emotion Speech Dataset",
    )
    HINDI_DATASET = Dataset(
        name="Hindi-Dataset",  # Vishal B. (2021). Speech Emotion Recognition (Hindi) Dataset. Kaggle.
        language=LANGUAGE.HINDI.value,
        url="vishlb/speech-emotion-recognition-hindi",
        path="ser_datasets/Hindi-Dataset/my Dataset",
    )
    IESC = Dataset(
        name="IESC",  # Indian English
        language=LANGUAGE.ENGLISH.value,
        url="ybsingh/indian-emotional-speech-corpora-iesc",
        path="ser_datasets/IESC",
    )
    KANNADA_DATASET = Dataset(
        name="Kannada-Dataset",
        language=LANGUAGE.KANNADA.value,
        url="thanikansivatheepan/kannada-emo-speech-dataset",
        path="ser_datasets/Kannada-Dataset",
    )
    MESD = Dataset(
        name="MESD",
        language=LANGUAGE.SPANISH.value,
        url="ashfaqsyed/mexican-emotional-speech-databasemesd",
        path="ser_datasets/MESD/cy34mh68j9-5/Mexican Emotional Speech Database (MESD)",
    )
    RAVDESS = Dataset(
        name="RAVDESS",
        language=LANGUAGE.ENGLISH.value,
        url="uwrfkaggler/ravdess-emotional-speech-audio",
        path="ser_datasets/RAVDESS",
    )
    SHEMO = Dataset(
        name="SHEMO",
        language=LANGUAGE.PERSIAN.value,
        url="mansourehk/shemo-persian-speech-emotion-detection-database",
        path="ser_datasets/SHEMO",
    )
    SUBESCO = Dataset(
        name="SUBESCO",
        language=LANGUAGE.BENGALI.value,
        url="sushmit0109/subescobangla-speech-emotion-dataset",
        path="ser_datasets/SUBESCO/SUBESCO",
    )
    SWAHILI_DATASET = Dataset(
        name="Swahili-Dataset",
        language=LANGUAGE.SWAHILI.value,
        url="luxluxshan/kenyan-swahili-ser",
        path="ser_datasets/Swahili-Dataset",
    )
    TELUGU_DATASET = Dataset(
        name="Telugu-Dataset",
        language=LANGUAGE.TELUGU.value,
        url="jettysowmith/telugu-emotion-speech",
        path="ser_datasets/Telugu-Dataset/telugu",
    )
    URDU_DATASET = Dataset(
        name="Urdu-Dataset",
        language=LANGUAGE.URDU.value,
        url="kingabzpro/urdu-emotion-dataset",
        path="ser_datasets/Urdu-Dataset",
    )
    KESDy18 = Dataset(
        name="KESDy18",
        language=LANGUAGE.KOREAN.value,
        url="luxluxshan/korean-emotional-speech-dataset-kesdy18",
        path="ser_datasets/KESDy18",
    )


class BASE_MODEL(Enum):
    WAV2VEC2_BASE = "facebook/wav2vec2-base"
    WAV2VEC2_LARGE_960H = "facebook/wav2vec2-large-960h"
    WAV2VEC2_LARGE_LV60 = "facebook/wav2vec2-large-lv60"
    HUBERT_LARGE_LS960 = "facebook/hubert-large-ls960-ft"
    HUBERT_BASE = "facebook/hubert-base-ls960"
    WAVLM_BASE_PLUS = "microsoft/wavlm-base-plus"
    WAVLM_LARGE = "microsoft/wavlm-large"
    XLS_R_300M = "facebook/wav2vec2-xls-r-300m"
    XLS_R_1B = "facebook/wav2vec2-xls-r-1b"
    OPENAI_WHISPER_SMALL = "openai/whisper-small"
    OPENAI_WHISPER_LARGE = "openai/whisper-large"
