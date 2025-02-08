from flask import Flask
from app.routes.llm import llm_bp
from app.routes.user import user_bp
from app.routes.usage import usage_bp
from app.routes.team import team_bp

api_version = "v1"


def register_routes(app: Flask):
    api_prefix = f"/api/{api_version}"
    app.register_blueprint(llm_bp, url_prefix=f"{api_prefix}/llm")
    app.register_blueprint(user_bp, url_prefix=f"{api_prefix}/user")
    app.register_blueprint(usage_bp, url_prefix=f"{api_prefix}/usage")
    app.register_blueprint(team_bp, url_prefix=f"{api_prefix}/team")
