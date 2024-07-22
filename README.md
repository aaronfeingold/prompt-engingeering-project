# Flask API Project - Prompt Engineering

## Project Overview

This Flask API project integrates OpenAI's language models for prompt engineering. It allows users to generate text based on prompts and stores responses in a PostgreSQL database.

## Features

- Generate AI-driven responses based on user prompts.
- Store prompt-response pairs along with metadata (response time, creation date).
- RESTful API endpoints for creating prompts and retrieving responses.

## Technologies Used

- Flask
- SQLAlchemy
- Python-dotenv
- Flask-Migrate
- OpenAI API

## Setup Instructions

1. **Clone Repository**:
    ```
    git clone https://github.com/aaronfeingold/prompt-engingeering-project
    cd prompt-engingeering-project
    ```
2. **Set Up Virtual Environment**:
    ```
    python -m venv venv
    source venv/bin/activate
    ```
3. **Install Dependencies**:
    ```
    pip install -r requirements.txt
    ```
4. **Setup Environment Variables**
- Create a .env file in the root directory
    ```
    DATABASE_URL=postgresql://username:password@localhost/dbname
    OPENAI_API_KEY=your-openai-api-key
    ```
5. **Database Migration**:
- Initialize migrations:
```
flask db init
```
- Generate a migration script:
```
flask db migrate -m "Initial migration"
```
- Apply the migration:
```
flask db upgrade
```
## Usage

- Create prompts using POST requests to `/prompt`.
- Retrieve stored prompts and responses using GET requests to `/prompts`.

## API Endpoints

- **POST `/prompt`**: Create a new prompt and generate a response.
- **GET `/prompts`**: Retrieve all stored prompts and responses.

## Testing/Debugging

**Test Suites**
- Run tests using `pytest` to ensure functionality and reliability.

**cURL Requests**
- When using Visual Studio Code Python File Debugger, these examples can used to interrogate endpoints:

```
curl -X POST http://127.0.0.1:5000/api/v1/openai/prompt -H "Content-Type: application/json" -d '{"prompt":"Write a short story about a brave knight who saves a village from a dragon."}'
```

and

```
curl http://127.0.0.1:5000/api/v1/openai/prompts -H "Content-Type: application/json"
```

## Deployment

- Deploy the Flask API project to a production environment using standard Flask deployment practices.

## Contributing

- Contributions are welcome! Please fork the repository and submit pull requests for new features or fixes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
