from openai import OpenAI


class OpenAIService:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_response(
        self, prompt, model="gpt-3.5-turbo", role="user", max_tokens=500
    ):
        return self.client.chat.completions.create(
            model=model,
            messages=[{"role": role, "content": prompt}],
            max_tokens=max_tokens,
        )
