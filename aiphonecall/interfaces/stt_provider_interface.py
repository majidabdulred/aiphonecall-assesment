from abc import ABC, abstractmethod
from enum import Enum
from typing import Union, BinaryIO


class STTProvider(ABC):
    """
    Abstract base class defining the interface for Speech-To-Text providers.

    This interface standardizes the interaction with various STT services like
    Deepgram and OpenAI. It defines the core functionality that
    all STT providers must implement while allowing for provider-specific
    customization through optional parameters.

    Attributes:
        api_key (str): Authentication key for the STT service.
    """

    def __init__(self, api_key: str):
        """
        Initialize the STT provider with authentication credentials.

        Args:
            api_key (str): Authentication key for the STT service.
        """
        self.api_key = api_key

    @abstractmethod
    def _create_payload(self, **kwargs) -> tuple[str, dict, BinaryIO]:
        """
        Create the API request payload for the STT service.

        Args:
            **kwargs: Arbitrary keyword arguments specific to the STT provider.

        Returns:
            tuple[str, dict, BinaryIO]: A tuple containing:
                - URL endpoint for the API request
                - Headers for the API request
                - File data payload for the API request . e.g. open('file.wav', 'rb')
        """
        pass

    @abstractmethod
    def speech2text(self,
                    filepath: str,
                    model: Union[str, Enum],
                    **kwargs) -> str:
        """
        Synchronously convert speech to text.

        Args:
            filepath (str): The path of the file that needs conversion.
            model (Union[str, Enum]): The model to use for speech to text conversion.
                Can be either a string identifier or provider-specific enum.
            **kwargs: Additional provider-specific parameters

        Returns:
            str: Returns the output text from the speech.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        pass

    @abstractmethod
    async def aspeech2text(self,
                           filepath: str,
                           model: Union[str, Enum],
                           **kwargs) -> str:
        """
        Asynchronously convert speech to text.

        Args:
            filepath (str): The path of the file that needs conversion.
            model (Union[str, Enum]): The model to use for speech to text conversion.
                Can be either a string identifier or provider-specific enum.
            **kwargs: Additional provider-specific parameters

        Returns:
            str: Returns the output text from the speech.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        pass
