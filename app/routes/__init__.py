from flask import Flask
from app.routes.openai import openai_bp
from app.routes.user import user_bp

api_version = "v1"


def register_routes(app: Flask):
    api_prefix = f"/api/{api_version}"
    app.register_blueprint(openai_bp, url_prefix=f"{api_prefix}/openai")
    app.register_blueprint(user_bp, url_prefix=f"{api_prefix}/user")
