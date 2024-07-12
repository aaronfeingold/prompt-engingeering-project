from flask import request, jsonify
from app import app, db
from models import PromptResponse
import openai
import time

openai.api_key = app.config['OPENAI_API_KEY']

@app.route('/prompt', methods=['POST'])
def create_prompt():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    start_time = time.time()
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    response_time = time.time() - start_time
    generated_text = response.choices[0].text.strip()

    prompt_response = PromptResponse(
        prompt=prompt,
        response=generated_text,
        response_time=response_time
    )
    db.session.add(prompt_response)
    db.session.commit()

    return jsonify({
        'id': prompt_response.id,
        'prompt': prompt_response.prompt,
        'response': prompt_response.response,
        'response_time': prompt_response.response_time,
        'created_at': prompt_response.created_at
    }), 201

@app.route('/prompts', methods=['GET'])
def get_prompts():
    prompts = PromptResponse.query.all()
    results = [
        {
            'id': prompt.id,
            'prompt': prompt.prompt,
            'response': prompt.response,
            'response_time': prompt.response_time,
            'created_at': prompt.created_at
        } for prompt in prompts
    ]
    return jsonify(results), 200
