from flask import Flask
from app.routes.prompts import bp

api_version = 'v1'


def register_routes(app: Flask):
    api_prefix = f'/api/{api_version}'
    app.register_blueprint(bp, url_prefix=f'{api_prefix}/prompt')
