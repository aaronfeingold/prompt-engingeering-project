from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from app.database import db
from app.services import OpenAIService
from app.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # todo: add migrations
    Migrate(app, db)
    # JWT Manager
    JWTManager(app)

    openai_service = OpenAIService(api_key=app.config["OPENAI_API_KEY"])
    app.openai_service = openai_service
    register_routes(app)

    return app
