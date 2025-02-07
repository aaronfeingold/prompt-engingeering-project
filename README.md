# Prompt Engineering 101

## Overview

This Flask API project integrates OpenAI's language models for prompt engineering. It allows users to generate _text_ based on prompts and stores responses in a PostgreSQL database.

## Features

- Generate AI-driven responses based on user prompts.
- Store prompt-response pairs along with metadata (response time, creation date).
- RESTful API endpoints for creating prompts and retrieving responses.
- OpenAI Usage Analysis
- User Budgeting Controls

## Tech Notes
- Flask API
- OpenAI API
- Postgres


## Setup Instructions

### Prequisite
- _Note_: Ansible on Fedora Workstation 39 installation will includes these deps and more. Click [here](https://github.com/aaronfeingold/ajf-fedora-workstation-ansible) for more details
- Python 3.11.10
- [Docker](#docker-instructions)
- Postgres
  - Create a new DB with creds
  - See [Environment Vars](#environment-variables) section
- Poetry

1. **Clone Repository**:
    ```
    git clone https://github.com/aaronfeingold/prompt-engingeering-project
    cd prompt-engingeering-project
    ```
2. **Virtual Environment**:
    ```
    poetry shell
    ```
3. **Install Dependencies**:
    ```
    poetry install
    ```
4. **Environment Variables**
- Create a .env file in the root directory
    ```
    DATABASE_URL=postgresql://username:password@localhost/dbname
    OPENAI_API_KEY=your-openai-api-key
    ```
5. **Database**:
- _Note_: check postgresql: `systemctl status postgresql`
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


## Deployment

## Docker Instructions

### Using Docker Compose

1. **Build and Start the Containers**:
    Navigate to the root directory of the project where the `docker-compose.yml` file is located and run the following command:
    ```sh
    docker-compose up --build -d
    ```
    This will build the Docker images and start the containers in detached mode.

2. **Environment Variables**:
    Ensure you have a `.env` file in the root directory with the necessary environment variables:
    ```env
    OPENAI_API_KEY=your-openai-api-key
    JWT_SECRET_KEY=your-jwt-secret-key
    JWT_ACCESS_TOKEN_EXPIRES=30
    ```

### Accessing the Flask App

3. **Access the Application**:
    You can now access the Flask app at `http://localhost:5000`. To test the endpoints, you can use tools like `curl` or Postman.

    Example using `curl`:
    ```sh
    curl -X POST http://localhost:5000/openai/prompt -d '{"prompt": "Hello, world!"}' -H "Content-Type: application/json"
    ```
    - _Note_: Postman project will soon be exported. Check back later.

### Stopping and Removing the Containers

4. **Stop the Containers**:
    To stop the running containers, use the following command:
    ```sh
    docker-compose down
    ```

### Additional Docker Compose Commands

- **View Logs**:
    To view the logs of the running containers, use:
    ```sh
    docker-compose logs
    ```

- **Access the Container Shell**:
    To access the shell of the running `api` container, use:
    ```sh
    docker-compose exec api /bin/sh
    ```

Make sure to replace the environment variable values in the [.env](http://_vscodecontentref_/1) file with your actual credentials.

## Contributing

- Contributions are welcome! Please fork the repository and submit pull requests for new features or fixes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
