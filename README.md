# Prompt Engineering 101

## Overview

This Flask API project integrates OpenAI's language models for prompt engineering. It allows users to generate _text_ based on prompts and stores responses in a PostgreSQL database.

## Features

- Generate AI-driven responses based on user prompts.
- Store prompt-response pairs along with metadata (response time, creation date).
- RESTful API endpoints for creating prompts and retrieving responses.

## Tech Notes

- Flask
- Flask-Migrate
- SQLAlchemy
- OpenAI API
- Poetry

## Setup Instructions

1. **Clone Repository**:
    ```
    git clone https://github.com/aaronfeingold/prompt-engingeering-project
    cd prompt-engingeering-project
    ```
2. **Set Up Virtual Environment**:
    ```
    poetry shell
    ```
3. **Install Dependencies**:
    ```
    poetry install
    ```
4. **Setup Environment Variables**
- Create a .env file in the root directory
    ```
    DATABASE_URL=postgresql://username:password@localhost/dbname
    OPENAI_API_KEY=your-openai-api-key
    ```
5. **Database Migrations**:
- Initialize:
```
flask db init
```
- Generate:
```
flask db migrate -m "Initial migration"
```
- Apply:
```
flask db upgrade
```

## Development

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. The hooks run `black` and `flake8`.

1. **Install pre-commit**:
    ```sh
    poetry run pre-commit install
    ```
2. **Run pre-commit hooks manually**:
    ```sh
    poetry run pre-commit run --all-files

## Usage



## Testing/Debugging

**Test Suites**
- Run tests using `pytest` to ensure functionality and reliability.

**cURL Requests**
- When using Visual Studio Code Python File Debugger, these examples can used to interrogate endpoints:

```
curl -X POST http://127.0.0.1:5000/api/v1/openai/prompt -H "Content-Type: application/json" -d '{"prompt_messages": [{"role": "user", "content": "Write a short story about a brave knight who saves a village from a dragon."}]}'
```

and

```
curl http://127.0.0.1:5000/api/v1/openai/prompt-responses -H "Content-Type: application/json"
```

## Deployment

- Deploy the Flask API project to a production environment using standard Flask deployment practices.

## Contributing

- Contributions are welcome! Please fork the repository and submit pull requests for new features or fixes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
