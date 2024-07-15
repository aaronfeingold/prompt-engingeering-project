from app.services import PromptResponseService


def create_new_prompt_response(client, prompt):
    return PromptResponseService.create_new_prompt_response(client, prompt)


def get_all_prompt_responses():
    return PromptResponseService.get_all_prompt_responses()
