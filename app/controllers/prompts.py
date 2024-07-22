from flask import jsonify
import openai
from app.services import PromptResponseService
import json


def create_new_prompt_response(request):
    prompt_messages = request.json.get("prompt_messages")
    if not prompt_messages:
        return jsonify({"error": "A Message is required"}), 400
    try:
        response_data = PromptResponseService.create_new_prompt_response(
            prompt_messages
        )

        return jsonify(response_data), 201
    except openai.RateLimitError as e:
        return (
            jsonify(
                {"error": f"API rate limit exceeded: {e}. Please try again later."}
            ),
            429,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An error occurred while processing your request",
                    "details": e,
                }
            ),
            500,
        )


def get_all_prompt_responses():
    try:
        return jsonify(PromptResponseService.get_all_prompt_responses()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
