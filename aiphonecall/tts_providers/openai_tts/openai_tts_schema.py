from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

@dataclass
class OpenAITTSVoices(Enum):
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"

@dataclass
class OpenAITTSModels(Enum):
    TTS_1 = "tts-1"
    TTS_1_HD = "tts-1-hd"

