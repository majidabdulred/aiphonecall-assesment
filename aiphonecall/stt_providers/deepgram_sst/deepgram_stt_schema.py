from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

@dataclass
class DeepgramSTTModels(Enum):
    NOVA = "nova"
    NOVA_2 = "nova-2"
    BASE = "base"
    ENHANCED = "enhanced"
