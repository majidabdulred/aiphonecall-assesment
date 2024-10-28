from abc import ABC, abstractmethod
from enum import Enum
from typing import IO, Union


class TTSProvider(ABC):
    """
    Abstract base class defining the interface for Text-to-Speech providers.

    This interface standardizes the interaction with various TTS services like
    Deepgram, ElevenLabs, and OpenAI. It defines the core functionality that
    all TTS providers must implement while allowing for provider-specific
    customization through optional parameters.

    Attributes:
        api_key (str): Authentication key for the TTS service.
    """

    def __init__(self, api_key: str):
        """
        Initialize the TTS provider with authentication credentials.

        Args:
            api_key (str): Authentication key for the TTS service.
        """
        self.api_key = api_key

    @abstractmethod
    def _create_payload(self, **kwargs) -> tuple[str, dict, dict]:
        """
        Create the API request payload for the TTS service.

        Args:
            **kwargs: Arbitrary keyword arguments specific to the TTS provider.

        Returns:
            tuple[str, dict, dict]: A tuple containing:
                - URL endpoint for the API request
                - Headers for the API request
                - Data payload for the API request
        """
        pass

    @abstractmethod
    def transcribe(self,
                   text: str,
                   voice: Union[str, Enum],
                   model: Union[str, Enum],
                   **kwargs) -> IO[bytes]:
        """
        Synchronously convert text to speech.

        Args:
            text (str): The text to convert to speech.
            voice (Union[str, Enum]): The voice to use for speech synthesis.
                Can be either a string identifier or provider-specific enum.
            model (Union[str, Enum]): The model to use for speech synthesis.
                Can be either a string identifier or provider-specific enum.
            **kwargs: Additional provider-specific parameters (e.g., stability,
                     similarity for ElevenLabs).

        Returns:
            IO[bytes]: A binary stream containing the generated audio.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        pass

    @abstractmethod
    async def atranscribe(self,
                          text: str,
                          voice: Union[str, Enum],
                          model: Union[str, Enum],
                          **kwargs) -> IO[bytes]:
        """
        Asynchronously convert text to speech.

        Args:
            text (str): The text to convert to speech.
            voice (Union[str, Enum]): The voice to use for speech synthesis.
                Can be either a string identifier or provider-specific enum.
            model (Union[str, Enum]): The model to use for speech synthesis.
                Can be either a string identifier or provider-specific enum.
            **kwargs: Additional provider-specific parameters (e.g., stability,
                     similarity for ElevenLabs).

        Returns:
            IO[bytes]: A binary stream containing the generated audio.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        pass