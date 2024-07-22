from openai import OpenAI


class OpenAIService:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, messages, model="gpt-3.5-turbo", max_tokens=500):
        """
        Generate a response from OpenAI API.

        :param messages: A list of message objects, each containing 'role' and 'content' keys.
        :param model: The model to use for generating responses.
        :param max_tokens: The maximum number of tokens to generate.
        :return: The response from OpenAI API.
        """

        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
        )
