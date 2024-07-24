from flask import current_app
import time
from app.models import PromptResponse, OpenAIUsage


class PromptResponseService:
    @staticmethod
    def create_new_prompt_response(prompts):
        """
        Generates a new prompt response using the OpenAI API,
        serializes the input prompt and the generated response,
        and stores them in the database.

        This method performs the following steps:
        1. Records the start time for generating a response.
        2. Calls the OpenAI API to generate a response based on the input prompts.
        3. Calculates the response time by subtracting the start time from the current time.
        4. Serializes both the input prompt and the generated response into JSON strings.
        5. Creates a new PromptResponse object with the serialized data and response time.
        6. Attempts to add the new PromptResponse object to the database.
        7. Returns a dictionary representation of the PromptResponse object.

        Parameters:
        - prompts (list/dict): The input prompt messages to send to the OpenAI API.

        Returns:
        - dict: A dictionary representation of the created PromptResponse object.

        Raises:
        - ValueError: If there is an issue creating the PromptResponse object.
        - RuntimeError: If there is an issue adding the PromptResponse object to the database
          or fetching its dictionary representation.
        """
        start_time = time.time()
        chat_completion = current_app.openai_service.generate_chat_completion(prompts)
        response_time = time.time() - start_time
        # always set responses to an array even if only 1 choice
        # destructure the object since there are other things in the
        # response which are not needed at this time
        responses = []
        if len(chat_completion.choices) == 1:
            responses = [
                {
                    "content": chat_completion.choices[0].message.content,
                    "role": chat_completion.choices[0].message.role,
                }
            ]
        else:
            for resp in chat_completion.choices:
                responses.append(
                    {"content": resp.message.content, "role": resp.message.role}
                )

        try:
            prompt_response = PromptResponse(
                prompts=prompts,
                responses=responses,
                response_time=response_time,
            )
            prompt_response.add_to_db()
        except Exception as e:
            raise RuntimeError(
                f"Failed to add prompt response to the database: {e}"
            ) from e

        try:
            usage_entry = OpenAIUsage(
                prompt_response_id=prompt_response.id,
                completion_tokens=chat_completion["completion_tokens"],
                prompt_tokens=chat_completion["prompt_tokens"],
                total_tokens=chat_completion["total_tokens"],
            )
            usage_entry.add_to_db()
        except Exception as e:
            raise RuntimeError(f"Failed to add usage data to the database: {e}")

        try:
            return prompt_response.to_dict()
        except Exception as e:
            raise RuntimeError(
                f"Failed to fetch prompt responses from the database: {e}"
            ) from e

    @staticmethod
    def query_prompt_responses(page, per_page, sort_by, sort_order):
        """
        Retrieves all prompt responses from the database and returns them as a list of dictionaries.

        This function performs a query to fetch all instances of PromptResponse from the database.
        Each PromptResponse object is then converted to a dictionary using its `to_dict` method.
        The list of these dictionaries is returned to the caller.

        Returns:
        - list: A list of dictionaries, where each dictionary represents a prompt response.

        Raises:
        - RuntimeError: If there is an issue fetching the prompt responses from the database.
        """

        try:
            query = PromptResponse.query

            if sort_order == "asc":
                query = query.order_by(getattr(PromptResponse, sort_by).asc())
            else:
                query = query.order_by(getattr(PromptResponse, sort_by).desc())

            paginated_responses = query.paginate(
                page=page, per_page=per_page, error_out=False
            )

            items = [item.to_dict() for item in paginated_responses.items]

            return {
                "page": paginated_responses.page,
                "per_page": paginated_responses.per_page,
                "total_pages": paginated_responses.pages,
                "total_items": paginated_responses.total,
                "items": items,
            }
        except Exception as e:
            raise RuntimeError(
                f"Failed to fetch prompt responses from the database: {e}"
            ) from e
