import time
from flask import request, jsonify
from app import app, db
from models import PromptResponse
import openai
from openai import OpenAI

client = OpenAI(api_key=app.config['OPENAI_API_KEY'])


def create_new_prompt_response(prompt):
    start_time = time.time()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    response_time = time.time() - start_time
    content, role = response.choices[0].message.content, response.choices[0].message.role

    prompt_response = PromptResponse(
        prompt=prompt,
        content=content,
        role=role,
        response_time=response_time
    )
    prompt_response.add_to_db()

    return prompt_response.to_dict()


def get_all_prompt_responses():
    prompt_responses = PromptResponse.query.all()

    return [response.to_dict() for response in prompt_responses]


@app.route('/prompt', methods=['POST'])
def create_prompt():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    try:
        response_data = create_new_prompt_response(prompt)

        return jsonify(response_data), 201
    except openai.RateLimitError as e:
        return jsonify({'error': f'API rate limit exceeded: {e}. Please try again later.'}), 429
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing your request', 'details': e}), 500


@app.route('/prompts', methods=['GET'])
def get_prompts():
    prompt_list = get_all_prompt_responses()

    return jsonify(prompt_list), 200
