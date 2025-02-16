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


class Dataset:
    name: str
    language: str
    path: str
    url: str
    feature_path: str

    def __init__(self, name, language, path, url, feature_path=None):
        self.name = name
        self.language = language
        self.path = path
        self.url = url
        self.feature_path = feature_path


class DATASET(Enum):
    ASED = Dataset(
        name="ASED",
        language=LANGUAGE.AMHARIC.value,
        url="thanikansivatheepan/amharic-speech-emotional-dataset-ased",
        path="datasets/ASED",
    )
    BANSPEMO = Dataset(
        name="BANSpEmo",
        language=LANGUAGE.BENGALI.value,
        url="thanikansivatheepan/bangla-lang-ser-dataset",
        path="datasets/BANSpEmo/BANSpEmo Dataset",
    )
    CAFE = Dataset(
        name="CaFE",
        language=LANGUAGE.FRENCH.value,
        url="jubeerathan/cafe-dataset",
        path="datasets/CaFE",
    )
    EMODB = Dataset(
        name="EmoDB",
        language=LANGUAGE.GERMAN.value,
        url="piyushagni5/berlin-database-of-emotional-speech-emodb",
        path="datasets/EmoDB/wav",
    )
    EMOTA = Dataset(
        name="EmoTa",
        language=LANGUAGE.TAMIL.value,
        url="luxluxshan/tamserdb",
        path="datasets/EmoTa",
        feature_path="data/features/ta_EmoTa_whisper_small.csv",
    )
    EMOVO = Dataset(
        name="EMOVO",
        language=LANGUAGE.ITALIAN.value,
        url="sourabhy/emovo-italian-ser-dataset",
        path="datasets/EMOVO/EMOVO",
    )
    ESD_CHINESE = Dataset(
        name="ESD",
        language=LANGUAGE.CHINESE.value,
        url="thanikansivatheepan/esd-dataset-fyp",
        path="datasets/ESD/Emotion Speech Dataset",
    )
    HINDI_DATASET = Dataset(
        name="Hindi-Dataset",
        language=LANGUAGE.HINDI.value,
        url="vishlb/speech-emotion-recognition-hindi",
        path="datasets/Hindi-Dataset/my Dataset",
    )
    KANNADA_DATASET = Dataset(
        name="Kannada-Dataset",
        language=LANGUAGE.KANNADA.value,
        url="thanikansivatheepan/kannada-emo-speech-dataset",
        path="datasets/Kannada-Dataset",
    )
    MESD = Dataset(
        name="MESD",
        language=LANGUAGE.SPANISH.value,
        url="ashfaqsyed/mexican-emotional-speech-databasemesd",
        path="datasets/MESD/cy34mh68j9-5/Mexican Emotional Speech Database (MESD)",
    )
    RAVDESS = Dataset(
        name="RAVDESS",
        language=LANGUAGE.ENGLISH.value,
        url="uwrfkaggler/ravdess-emotional-speech-audio",
        path="datasets/RAVDESS",
    )
    SUBESCO = Dataset(
        name="SUBESCO",
        language=LANGUAGE.BENGALI.value,
        url="sushmit0109/subescobangla-speech-emotion-dataset",
        path="datasets/SUBESCO/SUBESCO",
        feature_path="data/features/bn_SUBESCO_wavlm_base.csv",
    )
    TELUGU_DATASET = Dataset(
        name="Telugu-Dataset",
        language=LANGUAGE.TELUGU.value,
        url="jettysowmith/telugu-emotion-speech",
        path="datasets/Telugu-Dataset/telugu",
    )
    URDU_DATASET = Dataset(
        name="Urdu-Dataset",
        language=LANGUAGE.URDU.value,
        url="kingabzpro/urdu-emotion-dataset",
        path="datasets/Urdu-Dataset",
    )
