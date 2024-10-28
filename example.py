import asyncio

from aiphonecall.tts_providers import DeepgramTTSProvider, ElevenLabsTTSProvider, OpenAITTSProvider
from aiphonecall.tts_providers import DeepgramTTSModels, DeepgramTTSVoices, ElevenLabsTTSModels, ElevenLabTTSVoices, OpenAITTSModels, OpenAITTSVoices

from aiphonecall.stt_providers import DeepgramSTTProvider
from aiphonecall.stt_providers import DeepgramSTTModels

from aiphonecall.llm_providers import OpenAILLMProvider
from aiphonecall.llm_providers import OpenAILLMModels

from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API")
def example_tts():
    tts = ElevenLabsTTSProvider(ELEVENLABS_API_KEY)
    text = "Hi , How are you. I wanted to invite for the party tonight. If you are willing to come please respond soon."
    speech = tts.transcribe(text, model=ElevenLabsTTSModels.ELEVEN_TURBO_V2_5,voice=ElevenLabTTSVoices.ROGER)

    with open("output.mp3", "wb") as f:
        f.write(speech.read())

async def example_async_tts():
    tts = ElevenLabsTTSProvider(ELEVENLABS_API_KEY)
    text = "Hi , How are you. I wanted to invite for the party tonight. If you are willing to come please respond soon."
    speech = await tts.atranscribe(text, model=ElevenLabsTTSModels.ELEVEN_TURBO_V2_5, voice=ElevenLabTTSVoices.ROGER)

    with open("output.mp3", "wb") as f:
        f.write(speech.read())

def example_stt():
    stt = DeepgramSTTProvider(DEEPGRAM_API_KEY)
    file = "output.mp3"
    text = stt.speech2text(file,model=DeepgramSTTModels.ENHANCED)
    print(text)


async def example_async_stt():
    stt = DeepgramSTTProvider(DEEPGRAM_API_KEY)
    file = "output.mp3"
    text = await stt.aspeech2text(file, model=DeepgramSTTModels.ENHANCED)
    print(text)


def example_llm():
    llm = OpenAILLMProvider(OPENAI_API_KEY)
    response = llm.chat("What is Black Box problem?")
    print(response)


async def example_async_llm():
    llm = OpenAILLMProvider(OPENAI_API_KEY)
    response = await llm.achat("What is Black Box problem?")
    print(response)


if __name__ == "__main__":
    # example_llm()
    asyncio.run(example_async_llm())