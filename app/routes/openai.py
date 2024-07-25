from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.controllers import create_new_prompt_response, query_prompt_responses
from app.decorators import role_required

bp = Blueprint("openai", __name__)


@bp.route("/prompt", methods=["POST"])
@jwt_required()
@role_required(["admin", "user"])
def post_prompt():
    return create_new_prompt_response(request)


@bp.route("/prompt-responses", methods=["GET"])
@jwt_required()
@role_required(["admin", "user"])
def get_prompt_responses():
    return query_prompt_responses(request)
