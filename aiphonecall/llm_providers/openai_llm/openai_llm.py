import aiohttp
import requests

from aiphonecall.interfaces.llm_provider_interface import LLMProvider
from aiphonecall.utils.util import validate_str_value
from .openai_llm_schema import OpenAILLMModels


class OpenAILLMProvider(LLMProvider):
    """
    Openai implementation of the LLMProvider interface.

    Provides chat completion OPENAI API, using various models
    """

    def __init__(self, api_key):
        super().__init__(api_key)

    def _create_payload(self, **kwargs) -> tuple[str, dict, dict]:
        """
        Create the API request payload for OPENAI LLM service.

        Args:
            **kwargs: Must include 'text', 'temperature' and  'model'

        Returns:
            tuple[str, dict, dict]: URL, headers, and data payload for the API request

        """
        text = kwargs.get("text")
        temperature = kwargs.get("temperature")
        # Use the utility validation method to ensure the voice and model are valid and
        # convert them to enums if they are strings
        model = validate_str_value(OpenAILLMModels, kwargs.get("model"))

        url = f"https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json", }
        data = {
            "model": model.value,
            "temperature": temperature,
            "messages": [{"role": "system", "content": "You are a helpful assistant."},
                         {"role": "user", "content": text}]
        }

        return url, headers, data

    def chat(self,
             text: str,
             model: OpenAILLMModels | str = OpenAILLMModels.GPT_4o_MINI,
             temperature: float = 0.8,
             **kwargs) -> str:
        """
        Synchronously chats with the LLM.

        Args:
            text (str): The text to chat with the LLM.
            model (Union[str, OpenAILLMModels]): The model to use, defaults to GPT_4o_MINI.
            temperature (float): The randomness of the chat response.
            0.0 is deterministic, 1.0 is completely random.

        Returns:
            str: Returns the output text from the LLM.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        url, headers, data = self._create_payload(text=text, model=model, temperature=temperature)

        response = requests.post(url, headers=headers, json=data)
        if not response.ok:
            print(response.text)
            response.raise_for_status()
        text = response.json()['choices'][0]['message']['content']
        return text

    async def achat(self,
                    text: str,
                    model: OpenAILLMModels | str = OpenAILLMModels.GPT_4o_MINI,
                    temperature: float = 0.8,
                    **kwargs) -> str:
        """
        Asynchronously chats with the LLM.

        Args:
            text (str): The text to chat with the LLM.
            model (Union[str, OpenAILLMModels]): The model to use, defaults to GPT_4o_MINI.
            temperature (float): The randomness of the chat response.
            0.0 is deterministic, 1.0 is completely random.

        Returns:
            str: Returns the output text from the LLM.

        Raises:
            HTTPError: If the API request fails.
            ValueError: If invalid parameters are provided.
        """
        url, headers, data = self._create_payload(text=text, model=model, temperature=temperature)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if not response.ok:
                    print(response.text)
                    response.raise_for_status()  # Check if the request was successful
                response = await response.json()
                text = response['choices'][0]['message']['content']
                return text
