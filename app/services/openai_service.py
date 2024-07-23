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
        # Validate
        formatted_messages = []
        for message in messages:
            if "role" not in message or "content" not in message:
                raise ValueError("Each message must have 'role' and 'content' keys")
            if not isinstance(message["content"], str) or message["content"] == "":
                raise ValueError("The 'content' key must be a non-empty string")
            formatted_messages.append(
                {"role": message["role"], "content": message["content"]}
            )

        return self.client.chat.completions.create(
            model=model,
            messages=formatted_messages,
            max_tokens=max_tokens,
        )
