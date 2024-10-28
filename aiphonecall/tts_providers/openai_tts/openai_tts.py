import requests
from typing import IO
from io import BytesIO
from .openai_tts_schema import OpenAITTSModels, OpenAITTSVoices
from aiphonecall.interfaces.tts_provider_interface import TTSProvider
import aiohttp
from aiphonecall.utils.util import validate_str_value


class OpenAITTSProvider(TTSProvider):
    """
    Openai implementation of the TTSProvider interface.

    Provides text-to-speech conversion using the OPENAI API, using various
    models and voices
    """

    def __init__(self, api_key):
        super().__init__(api_key)

    def _create_payload(self, **kwargs) -> tuple[str, dict, dict]:
        """
        Create the API request payload for OPENAI TTS service.

        Args:
            **kwargs: Must include 'text', 'voice' and  'model'

        Returns:
            tuple[str, dict, dict]: URL, headers, and data payload for the API request

        """
        text = kwargs.get("text")
        # Use the utility validation method to ensure the voice and model are valid and
        # convert them to enums if they are strings
        voice = validate_str_value(OpenAITTSVoices, kwargs.get("voice"))
        model = validate_str_value(OpenAITTSModels, kwargs.get("model"))

        url = f"https://api.openai.com/v1/audio/speech"
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json"}
        data = {
            "model": model.value,
            "voice": voice.value,
            "input": text
        }
        return url, headers, data

    def transcribe(self,
                   text: str,
                   voice: OpenAITTSVoices | str = OpenAITTSVoices.ALLOY,
                   model: OpenAITTSModels | str = OpenAITTSModels.TTS_1_HD,
                   **kwargs) -> IO[bytes]:
        """
        Synchronously convert text to speech using OPENAI API.

        Args:
            text (str): The text to convert to speech.
            voice (Union[str, OpenAITTSVoices]): The voice to use, defaults to ALLOY.
            model (Union[str, OpenAITTSModels]): The model to use, defaults to TTS_1_HD.

        Returns:
            IO[bytes]: A binary stream containing the generated audio.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        url, headers, data = self._create_payload(text=text, voice=voice, model=model)

        response = requests.post(url, headers=headers, json=data, stream=True)
        if not response.ok:
            print(response.text)
            response.raise_for_status()
        audio_stream = BytesIO(response.content)

        return audio_stream

    async def atranscribe(self,
                          text: str,
                          voice: OpenAITTSVoices | str = OpenAITTSVoices.ALLOY,
                          model: OpenAITTSModels | str = OpenAITTSModels.TTS_1_HD,
                          **kwargs) -> IO[bytes]:
        """
        Asynchronously convert text to speech using OPENAI API.

        Args:
            text (str): The text to convert to speech.
            voice (Union[str, OpenAITTSVoices]): The voice to use, defaults to ALLOY.
            model (Union[str, OpenAITTSModels]): The model to use, defaults to TTS_1_HD.

        Returns:
            IO[bytes]: A binary stream containing the generated audio.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        url, headers, data = self._create_payload(text=text, voice=voice, model=model)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if not response.ok:
                    print(response.text)
                    response.raise_for_status()
                audio_stream = BytesIO(await response.content.read())
                return audio_stream
