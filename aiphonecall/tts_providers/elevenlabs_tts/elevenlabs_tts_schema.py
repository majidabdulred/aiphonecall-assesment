from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

@dataclass
class ElevenLabTTSVoices(Enum):
    ARIA = "9BWtsMINqrJLrRacOk9x"
    ROGER = "CwhRBWXzGAHq8TQ4Fs17"
    SARAH = "EXAVITQu4vr4xnSDxMaL"
    LAURA = "FGY2WhTYpPnrIDTdsKH5"
    CHARLIE = "IKne3meq5aSn9XLyUdCD"
    GEORGE = "JBFqnCBsd6RMkjVDRZzb"
    CALLUM = "N2lVS1w4EtoT3dr4eOWO"
    RIVER = "SAz9YHcvj6GT2YYXdXww"
    LIAM = "TX3LPaxmHKxFdv7VOQHJ"
    CHARLOTTE = "XB0fDUnXU5powFXDhCwa"
    ALICE = "Xb7hH8MSUJpSbSDYk0k2"
    MATILDA = "XrExE9yKIg1WjnnlVkGX"
    WILL = "bIHbv24MWmeRgasZH58o"
    JESSICA = "cgSgspJ2msm6clMCkdW9"
    ERIC = "cjVigY5qzO86Huf0OWal"
    CHRIS = "iP95p4xoKVk53GoZ742B"
    BRIAN = "nPczCjzI2devNBz1zQrb"
    DANIEL = "onwK4e9ZLuTAKqWW03F9"
    LILY = "pFZP5JQG7iQjIQuC4Bku"
    BILL = "pqHfZKP75CvOlQylNhV4"

@dataclass
class ElevenLabsTTSModels(Enum):
    ELEVEN_MULTILINGUAL_V2 = "eleven_multilingual_v2"
    ELEVEN_TURBO_V2_5 = "eleven_turbo_v2_5"
    ELEVEN_TURBO_V2 = "eleven_turbo_v2"
    ELEVEN_MULTILINGUAL_V1 = "eleven_multilingual_v1"
    ELEVEN_MONOLINGUAL_V1 = "eleven_monolingual_v1"

