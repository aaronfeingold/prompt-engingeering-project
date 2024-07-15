import pytest
from app import app, db
from models import PromptResponse

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_create_prompt(client):
    # Define a sample prompt data
    prompt_data = {
        'prompt': 'Test prompt'
    }

    # Send a POST request to the /prompt endpoint
    response = client.post('/prompt', json=prompt_data)

    # Assert the response status code
    assert response.status_code == 201

    # Assert the response JSON content
    json_data = response.get_json()
    assert 'id' in json_data
    assert 'prompt' in json_data
    assert 'response' in json_data
    assert 'response_time' in json_data
    assert 'created_at' in json_data

def test_create_prompt_missing_prompt(client):
    # Send a POST request without the 'prompt' field
    response = client.post('/prompt', json={})

    # Assert the response status code
    assert response.status_code == 400

    # Assert the error message
    json_data = response.get_json()
    assert 'error' in json_data
    assert json_data['error'] == 'Prompt is required'

def test_get_prompts(client):
    # Send a GET request to the /prompts endpoint
    response = client.get('/prompts')

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response JSON content (assuming there are no prompts initially)
    json_data = response.get_json()
    assert isinstance(json_data, list)

def test_create_prompt_rate_limit_exceeded(client, monkeypatch):
    # Mocking OpenAI API client to raise RateLimitError
    def mock_create(*args, **kwargs):
        raise openai.RateLimitError(message="API rate limit exceeded")

    monkeypatch.setattr('openai.ChatCompletion.create', mock_create)

    # Send a POST request to the /prompt endpoint
    response = client.post('/prompt', json={'prompt': 'Test prompt'})

    # Assert the response status code
    assert response.status_code == 429

    # Assert the error message
    json_data = response.get_json()
    assert 'error' in json_data
    assert json_data['error'] == 'API rate limit exceeded. Please try again later.'
