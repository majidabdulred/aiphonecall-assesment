import requests
from typing import IO
from io import BytesIO
from .elevenlabs_tts_schema import ElevenLabTTSVoices, ElevenLabsTTSModels
from aiphonecall.interfaces.tts_provider_interface import TTSProvider
import aiohttp
from aiphonecall.utils.util import validate_str_value


class ElevenLabsTTSProvider(TTSProvider):
    """
    ElevenLabs implementation of the TTSProvider interface.

    Provides text-to-speech conversion using the ElevenLabs API, using various models and voices,
    and voice settings like stability and similarity.
    """

    def __init__(self, api_key):
        super().__init__(api_key)

    def _create_payload(self, **kwargs) -> tuple[str, dict, dict]:
        """
        Create the API request payload for ElevenLabs TTS service.

        Args:
            **kwargs: Must include 'text', 'voice', 'model', and optionally
                     'stability' and 'similarity' parameters.

        Returns:
            tuple[str, dict, dict]: URL, headers, and data payload for the API request

        """
        text = kwargs.get("text")
        stability = kwargs.get("stability")
        similarity = kwargs.get("similarity")
        # Use the utility validation method to ensure the voice and model are valid and
        # convert them to enums if they are strings
        voice = validate_str_value(ElevenLabTTSVoices, kwargs.get("voice"))
        model = validate_str_value(ElevenLabsTTSModels, kwargs.get("model"))

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice.value}/stream"
        headers = {"xi-api-key": self.api_key}
        data = {
            "text": text,
            "model_id": model.value,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }
        return url, headers, data

    def transcribe(self,
                   text: str,
                   voice: ElevenLabTTSVoices | str = "DANIEL",
                   model: ElevenLabsTTSModels | str = "eleven_turbo_v2_5",
                   stability: float = 0.5,
                   similarity: float = 0.8) -> IO[bytes]:
        """
        Synchronously convert text to speech using ElevenLabs.

        Args:
            text (str): The text to convert to speech.
            voice (Union[str, ElevenLabTTSVoices]): The voice to use, defaults to DANIEL.
            model (Union[str, ElevenLabsModels]): The model to use, defaults to eleven_turbo_v2_5.
            stability (float): Voice stability (0.0-1.0), defaults to 0.5
            similarity (float): Voice similarity boost (0.0-1.0), defaults to 0.8

        Returns:
            IO[bytes]: A binary stream containing the generated audio.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        url, headers, data = self._create_payload(text=text, voice=voice, model=model, stability=stability,
                                                  similarity=similarity)

        response = requests.post(url, headers=headers, json=data, stream=True)
        if not response.ok:
            print(response.text)
            response.raise_for_status()
        audio_stream = BytesIO()
        # Read the response in chunks and write to BytesIO
        for chunk in response:
            if chunk:
                audio_stream.write(chunk)
        audio_stream.seek(0)
        return audio_stream

    async def atranscribe(self,
                          text: str,
                          voice: ElevenLabTTSVoices | str = ElevenLabTTSVoices.DANIEL,
                          model: ElevenLabsTTSModels | str = ElevenLabsTTSModels.ELEVEN_TURBO_V2_5,
                          stability: float = 0.5,
                          similarity: float = 0.8) -> IO[bytes]:

        """
        Asynchronously convert text to speech using ElevenLabs.

        Args:
            text (str): The text to convert to speech.
            voice (Union[str, ElevenLabTTSVoices]): The voice to use, defaults to DANIEL.
            model (Union[str, ElevenLabsModels]): The model to use, defaults to eleven_turbo_v2_5.
            stability (float): Voice stability (0.0-1.0), defaults to 0.5
            similarity (float): Voice similarity boost (0.0-1.0), defaults to 0.8

        Returns:
            IO[bytes]: A binary stream containing the generated audio.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        url, headers, data = self._create_payload(text=text, voice=voice, model=model, stability=stability,
                                                  similarity=similarity)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                response.raise_for_status()

                audio_stream = BytesIO()
                # Asynchronously read the response in chunks and write to BytesIO
                async for chunk in response.content.iter_any():
                    audio_stream.write(chunk)

                # Reset the BytesIO stream position to the beginning
                audio_stream.seek(0)
                return audio_stream
