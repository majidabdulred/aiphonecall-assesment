from dataclasses import dataclass
from enum import Enum

@dataclass
class DeepgramTTSVoices(Enum):
    ASTERIA = "asteria"
    LUNA = "luna"
    STELLA = "stella"
    ATHENA = "athena"
    HERA = "hera"
    ORION = "orion"
    ARCAS = "arcas"
    PERSEUS = "perseus"
    ANGUS = "angus"
    ORPHEUS = "orpheus"
    HELIOS = "helios"
    ZEUS = "zeus"

@dataclass
class DeepgramTTSModels(Enum):
    AURA = "aura"

