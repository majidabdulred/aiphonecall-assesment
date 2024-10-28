import requests
from typing import IO, Tuple, Dict, BinaryIO
from io import BytesIO
import aiohttp
from .deepgram_stt_schema import DeepgramSTTModels
from aiphonecall.interfaces.stt_provider_interface import STTProvider
from aiphonecall.utils.util import validate_str_value
import os


class DeepgramSTTProvider(STTProvider):
    """
    Deepgram implementation of the STTProvider interface.

    Provides speech-to-text conversion using the Deepgram API, using various models.
    """

    def __init__(self, api_key):
        super().__init__(api_key)

    def _create_payload(self, **kwargs) -> tuple[str, dict, BinaryIO]:
        """
        Create the API request payload for Deepgram STT service.

        Args:
            **kwargs: Must include 'filepath' and  'model'

        Returns:
            tuple[str, dict, BinaryIO]: URL, headers, and data payload for the API request

        """
        filepath = kwargs.get("filepath")
        # Use the utility validation method to ensure the voice and model are valid and
        # convert them to enums if they are strings
        model = validate_str_value(DeepgramSTTModels, kwargs.get("model"))

        url = f"https://api.deepgram.com/v1/listen?model={model.value}&smart_format=true"
        headers = {"Authorization": f"Token {self.api_key}",
                   "Content-Type": "audio/*"}
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found at {filepath}")
        data = open(filepath, "rb")
        return url, headers, data

    def speech2text(self,
                    filepath: str,
                    model: DeepgramSTTModels | str = DeepgramSTTModels.NOVA_2,
                    **Kwargs) -> str:
        """
        Synchronously convert speech to text.

        Args:
            filepath (str): The path of the file that needs conversion.
            model (DeepgramSTTModels[str, Enum]): The model to use, defaults to NOVA_2.



        Returns:
            str: Returns the output text from the speech.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        url, headers, data = self._create_payload(filepath=filepath, model=model)

        response = requests.post(url, headers=headers, data=data)
        if not response.ok:
            print(response.text)
            response.raise_for_status()
        text = response.json()['results']["channels"][0]["alternatives"][0]["transcript"]
        return text

    async def aspeech2text(self,
                           filepath: str,
                           model: DeepgramSTTModels | str = DeepgramSTTModels.NOVA_2,
                           **kwargs) -> str:
        """
        Asynchronously convert speech to text.

        Args:
            filepath (str): The path of the file that needs conversion.
            model (DeepgramSTTModels[str, Enum]): The model to use, defaults to NOVA_2.

        Returns:
            str: Returns the output text from the speech.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        url, headers, data = self._create_payload(filepath=filepath, model=model)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if not response.ok:
                    print(response.text)
                    response.raise_for_status()  # Check if the request was successful
                response = await response.json()
                text = response['results']["channels"][0]["alternatives"][0]["transcript"]
                return text
