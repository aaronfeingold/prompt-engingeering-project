import time
from app.models import PromptResponse


class PromptResponseService:
    @staticmethod
    def create_new_prompt_response(openai_service, prompt):
        start_time = time.time()
        response = openai_service.generate_response(prompt)
        response_time = time.time() - start_time
        content, role = response.choices[0].message.content, response.choices[0].message.role

        prompt_response = PromptResponse(
            prompt=prompt,
            content=content,
            role=role,
            response_time=response_time
        )
        prompt_response.add_to_db()  # Assuming this method adds the object to the DB and commits the session
        return prompt_response.to_dict()

    @staticmethod
    def get_all_prompt_responses():
        prompt_responses = PromptResponse.query.all()
        return [response.to_dict() for response in prompt_responses]
