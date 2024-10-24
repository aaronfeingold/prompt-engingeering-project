from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.controllers import create_new_prompt_response, query_prompt_responses
from app.decorators import role_required, validate_schema, PromptResponseSchema
from app.models.user import RoleEnum

openai_bp = Blueprint("openai", __name__)


@openai_bp.route("/prompt", methods=["POST"])
@jwt_required()
@role_required([RoleEnum.USER, RoleEnum.ADMIN])
@validate_schema(PromptResponseSchema())
def post_prompt():
    return create_new_prompt_response(request)


@openai_bp.route("/prompt-responses", methods=["GET"])
@jwt_required()
@role_required([RoleEnum.USER, RoleEnum.ADMIN])
def get_prompt_responses():
    return query_prompt_responses(request)
