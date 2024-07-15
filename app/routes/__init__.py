from flask import Flask
from .prompts import prompts

api_version = 'v1'


def register_routes(app: Flask, openai_service):
    api_prefix = f'/api/{api_version}'
    app.register_blueprint(prompts, url_prefix=f'{api_prefix}/prompt')
