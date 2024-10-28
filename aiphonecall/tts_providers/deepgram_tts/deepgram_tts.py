import requests
from typing import IO
from io import BytesIO
from .deepgram_tts_schema import DeepgramTTSModels, DeepgramTTSVoices
from aiphonecall.interfaces.tts_provider_interface import TTSProvider
import aiohttp
from aiphonecall.utils.util import validate_str_value


class DeepgramTTSProvider(TTSProvider):
    """
    Deepgram implementation of the TTSProvider interface.

    Provides text-to-speech conversion using the Deepgram API, using various models and voices
    """

    def __init__(self, api_key):
        super().__init__(api_key)

    def _create_payload(self, **kwargs) -> tuple[str, dict, dict]:
        """
        Create the API request payload for Deepgram TTS service.

        Args:
            **kwargs: Must include 'text', 'voice' and  'model'

        Returns:
            tuple[str, dict, dict]: URL, headers, and data payload for the API request

        """
        text = kwargs.get("text")
        # Use the utility validation method to ensure the voice and model are valid and
        # convert them to enums if they are strings
        voice = validate_str_value(DeepgramTTSVoices, kwargs.get("voice"))
        model = validate_str_value(DeepgramTTSModels, kwargs.get("model"))

        url = f"https://api.deepgram.com/v1/speak?model={model.value}-{voice.value}-en"
        headers = {"Authorization": f"Token {self.api_key}"}
        data = {
            "text": text,
        }
        return url, headers, data

    def transcribe(self,
                   text: str,
                   voice: DeepgramTTSVoices | str = DeepgramTTSVoices.ARCAS,
                   model: DeepgramTTSModels | str = DeepgramTTSModels.AURA,
                   **kwargs) -> IO[bytes]:
        """
        Synchronously convert text to speech using Deepgram API.

        Args:
            text (str): The text to convert to speech.
            voice (Union[str, DeepgramTTSVoices]): The voice to use, defaults to ARCAS.
            model (Union[str, DeepgramTTSModels]): The model to use, defaults to AURA.

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

        # Convert the response content to a BytesIO stream
        audio_stream = BytesIO(response.content)

        return audio_stream

    async def atranscribe(self,
                          text: str,
                          voice: DeepgramTTSVoices | str = DeepgramTTSVoices.ARCAS,
                          model: DeepgramTTSModels | str = DeepgramTTSModels.AURA,
                          **kwargs) -> IO[bytes]:
        """
        Asynchronously convert text to speech using Deepgram API.

        Args:
            text (str): The text to convert to speech.
            voice (Union[str, DeepgramTTSVoices]): The voice to use, defaults to ARCAS.
            model (Union[str, DeepgramTTSModels]): The model to use, defaults to AURA.

        Returns:
            IO[bytes]: A binary stream containing the generated audio.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        url, headers, data = self._create_payload(text=text, voice=voice, model=model)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                response.raise_for_status()  # Check if the request was successful

                audio_stream = BytesIO(await response.content.read())
                return audio_stream
