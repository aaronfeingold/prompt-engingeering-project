from flask import current_app
import time
from app.models import PromptResponse
import json


class PromptResponseService:
    @staticmethod
    def create_new_prompt_response(prompt_messages):
        start_time = time.time()
        response = current_app.openai_service.generate_response(prompt_messages)
        response_time = time.time() - start_time
        content, role = response.choices[0].message.content, response.choices[0].message.role
        try:
            prompt_json = json.dumps(prompt_messages)
            messages_json = json.dumps({"content": content, "role": role})
            prompt_response = PromptResponse(
                prompt=prompt_json,
                messages=messages_json,
                response_time=response_time,
            )
        except Exception as e:
            raise ValueError(f"Failed to create prompt response: {e}") from e

        try:
            prompt_response.add_to_db()
        except Exception as e:
            raise RuntimeError(
                f"Failed to add prompt response to the database: {e}"
            ) from e

        try:
            return prompt_response.to_dict()
        except Exception as e:
            raise RuntimeError(
                f"Failed to fetch prompt responses from the database: {e}"
            ) from e

    @staticmethod
    def get_all_prompt_responses():
        try:
            prompt_responses = PromptResponse.query.all()
            return [response.to_dict() for response in prompt_responses]
        except Exception as e:
            raise RuntimeError(
                f"Failed to fetch prompt responses from the database: {e}"
            ) from e
