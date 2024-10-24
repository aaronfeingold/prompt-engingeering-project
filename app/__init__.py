from flask import Flask
from flask_migrate import Migrate, upgrade
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, text
from config import Config
from app.database import db
from app.services import OpenAIService
from app.routes import register_routes

bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # todo: add migrations
    Migrate(app, db)
    # Bcrypt passwords for now
    bcrypt.init_app(app)
    # JWT Manager
    JWTManager(app)

    check_and_create_database(app.config["SQLALCHEMY_DATABASE_URI"])
    # After creating the database, run migrations
    with app.app_context():
        upgrade()  # This will apply any pending migrations

    openai_service = OpenAIService(api_key=app.config["OPENAI_API_KEY"])
    app.openai_service = openai_service
    register_routes(app)

    return app


def check_and_create_database(database_url):
    # Extract the database name from the URL
    db_name = database_url.split("/")[-1]
    base_url = database_url.rsplit("/", 1)[0] + "/postgres"
    # Connect to the PostgreSQL server
    engine = create_engine(base_url, isolation_level="AUTOCOMMIT")

    # Use the 'postgres' database to create the new database
    with engine.connect() as connection:
        # Check if the database exists
        result = connection.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": db_name},
        )
        exists = result.fetchone()

        if not exists:
            # If it doesn't exist, create the database
            connection.execute(text(f"CREATE DATABASE {db_name}"))
            print(f"Database '{db_name}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")
