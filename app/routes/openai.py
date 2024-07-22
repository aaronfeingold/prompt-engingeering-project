from flask import Blueprint, request, jsonify
from app.controllers import create_new_prompt_response, get_all_prompt_responses


bp = Blueprint("prompts", __name__)


@bp.route("/prompt", methods=["POST"])
def post_prompt():
    return create_new_prompt_response(request)


@bp.route("/prompt-responses", methods=["GET"])
def get_prompt_responses():
    return get_all_prompt_responses()
