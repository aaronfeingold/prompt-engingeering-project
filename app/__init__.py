from flask import Flask
from flask_migrate import Migrate
from config import Config
from app.database import db
from app.services import OpenAIService
from app.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    openai_service = OpenAIService(api_key=app.config['OPENAI_API_KEY'])
    register_routes(app, openai_service)

    return app
