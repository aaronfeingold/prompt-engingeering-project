from openai import OpenAI
from app.constants import DEFAULT_MODEL, DEFAULT_MAX_TOKENS


class OpenAIService:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_chat_completion(
        self, prompt_messages, model=DEFAULT_MODEL, max_tokens=DEFAULT_MAX_TOKENS, n=1
    ):
        """
        Generate a response from OpenAI API.

        :param prompt_messages: A list of message objects, each containing 'role' and 'content' keys.
        :param model: The model to use for generating responses.
        :param max_tokens: The maximum number of tokens to generate.
        :return: The response from OpenAI API.
        """

        return self.client.chat.completions.create(
            model=model, messages=prompt_messages, max_tokens=max_tokens, n=n
        )
