from flask import request, jsonify
from app import app, db
from models import PromptResponse
import openai
from openai import OpenAI

client = OpenAI(api_key=app.config['OPENAI_API_KEY'])
import time


@app.route('/prompt', methods=['POST'])
def create_prompt():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        response_time = time.time() - start_time
        generated_text = response.choices[0].message

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
    except openai.RateLimitError as e:
        return jsonify({'error': 'API rate limit exceeded. Please try again later.'}), 429
    except Exception as e:
            return jsonify({'error': 'An error occurred while processing your request.', 'details': error_message}), 500

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
