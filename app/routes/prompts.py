from flask import Blueprint, request, jsonify
from app.controllers import create_new_prompt_response, get_all_prompt_responses
import openai

bp = Blueprint('prompts', __name__)


@bp.route('/prompt', methods=['POST'])
def create_prompt_response():
    prompt = request.json.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    try:
        response_data = create_new_prompt_response(app.openai_service, prompt)

        return jsonify(response_data), 201
    except openai.RateLimitError as e:
        return jsonify({'error': f'API rate limit exceeded: {e}. Please try again later.'}), 429
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing your request', 'details': e}), 500


@bp.route('/prompts', methods=['GET'])
def get_prompt_responses():
    prompt_list = get_all_prompt_responses()

    return jsonify(prompt_list), 200
