from flask import current_app
import time
from app.models import PromptResponse


class PromptResponseService:
    @staticmethod
    def create_new_prompt_response(messages):
        start_time = time.time()
        response = current_app.openai_service.generate_response(messages)
        response_time = time.time() - start_time
        content, role = response.choices[0].message.content, response.choices[0].message.role

        prompt_response = PromptResponse(
            prompt=messages, content=content, role=role, response_time=response_time
        )
        prompt_response.add_to_db()
        return prompt_response.to_dict()

    @staticmethod
    def get_all_prompt_responses():
        try:
            prompt_responses = PromptResponse.query.all()
            return [response.to_dict() for response in prompt_responses]
        except Exception as e:
            raise RuntimeError(
                f"Failed to fetch prompt responses from the database: {e}"
            ) from e
