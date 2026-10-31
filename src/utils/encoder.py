def emotion_converter(value, EMOTION_MAPPING, mode="encode"):
    if mode == "encode":
        if value not in EMOTION_MAPPING:
            raise ValueError(
                f"Invalid emotion: {value}. "
                f"Allowed values are {list(EMOTION_MAPPING)}"
            )
        return EMOTION_MAPPING[value], EMOTION_MAPPING
    if mode == "decode":
        for emotion, idx in EMOTION_MAPPING.items():
            if idx == value:
                return emotion
        raise ValueError(
            f"Invalid encoded value: {value}. "
            f"Allowed values are {list(EMOTION_MAPPING.values())}"
        )
    raise ValueError("Mode should be either 'encode' or 'decode'")
