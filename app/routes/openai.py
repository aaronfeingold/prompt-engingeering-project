from flask import Blueprint, request
from app.controllers import create_new_prompt_response, query_prompt_responses
from app.decorators import role_required

bp = Blueprint("openai", __name__)


@bp.route("/prompt", methods=["POST"])
@role_required(["admin", "user"])
def post_prompt():
    return create_new_prompt_response(request)


@bp.route("/prompt-responses", methods=["GET"])
@role_required(["admin", "user"])
def get_prompt_responses():
    return query_prompt_responses(request)
