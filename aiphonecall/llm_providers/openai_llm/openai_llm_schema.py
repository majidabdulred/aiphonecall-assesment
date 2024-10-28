from dataclasses import dataclass
from enum import Enum

@dataclass
class OpenAILLMModels(Enum):
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_35_TURBO = "gpt-3.5-turbo"
    GPT_4o = "gpt-4o"
    GPT_4 = "gpt-4"
    GPT_4o_MINI = "gpt-4o-mini"
