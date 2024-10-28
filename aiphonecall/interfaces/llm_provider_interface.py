from abc import ABC, abstractmethod
from enum import Enum
from typing import Union


class LLMProvider(ABC):
    """
    Abstract base class defining the interface for LLM providers.

    This interface standardizes the interaction with various LLM services like
    OpenAI. It defines the core functionality that
    all LLM providers must implement while allowing for provider-specific
    customization through optional parameters.

    Attributes:
        api_key (str): Authentication key for the LLM service.
    """

    def __init__(self, api_key: str):
        """
        Initialize the LLM provider with authentication credentials.

        Args:
            api_key (str): Authentication key for the LLM service.
        """
        self.api_key = api_key

    @abstractmethod
    def _create_payload(self, **kwargs) -> tuple[str, dict, dict]:
        """
        Create the API request payload for the LLM service.

        Args:
            **kwargs: Arbitrary keyword arguments specific to the LLM provider.

        Returns:
            tuple[str, dict, dict]: A tuple containing:
                - URL endpoint for the API request
                - Headers for the API request
                - Data payload for the API request
        """
        pass

    @abstractmethod
    def chat(self,
             text: str,
             model: Union[str, Enum],
             **kwargs) -> str:
        """
        Synchronously chat with the LLM.

        Args:
            text (str): Your message to chat with the LLM.
            model (Union[str, Enum]): The LLM model to use for conversation.
                Can be either a string identifier or provider-specific enum.
            **kwargs: Additional provider-specific parameters

        Returns:
            str: Returns the output text from the LLM.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        pass

    @abstractmethod
    async def achat(self,
                    text: str,
                    model: Union[str, Enum],
                    **kwargs) -> str:
        """
        Asynchronously chat with the LLM.

        Args:
            text (str): Your message to chat with the LLM.
            model (Union[str, Enum]): The LLM model to use for conversation.
                Can be either a string identifier or provider-specific enum.
            **kwargs: Additional provider-specific parameters

        Returns:
            str: Returns the output text from the LLM.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        pass
