from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers import create_new_prompt_response, query_prompt_responses
from app.decorators import role_required

openai_bp = Blueprint("openai", __name__)


@openai_bp.route("/prompt", methods=["POST"])
@jwt_required()
@role_required(["admin", "user"])
def post_prompt():
    user_identity = get_jwt_identity()
    return create_new_prompt_response(request, user_identity)


@openai_bp.route("/prompt-responses", methods=["GET"])
@jwt_required()
@role_required(["admin", "user"])
def get_prompt_responses():
    user_identity = get_jwt_identity()
    user_list = request.args.getlist("users")
    return query_prompt_responses(request, user_identity, user_list)
