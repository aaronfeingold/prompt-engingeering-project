from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import request, jsonify
from marshmallow import Schema, fields, ValidationError
from app.models import User
from app.constants import DEFAULT_MODEL, DEFAULT_MAX_TOKENS


def role_required(required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user.role not in required_roles:
                return (
                    jsonify({"message": "Access forbidden: insufficient permissions"}),
                    403,
                )
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def validate_prompt_messages(prompt_messages):
    for message in prompt_messages:
        if "role" not in message or "content" not in message:
            raise ValidationError("Each message must have 'role' and 'content' keys")
        if not isinstance(message["content"], str) or message["content"] == "":
            raise ValidationError("The 'content' key must be a non-empty string")


class PromptResponseSchema(Schema):
    prompt_messages = fields.List(
        fields.Dict(required=True), required=True, validate=validate_prompt_messages
    )
    team_id = fields.Str(required=True)
    model = fields.Str(missing=DEFAULT_MODEL)
    max_tokens = fields.Int(missing=DEFAULT_MAX_TOKENS)


# Create the validation decorator
def validate_schema(schema: Schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Validate and deserialize input
                validated_data = schema.load(request.json)
                # Attach validated data to request for use in the endpoint
                request.validated_data = validated_data
                return func(*args, **kwargs)
            except ValidationError as err:
                return jsonify({"errors": err.messages}), 400

        return wrapper

    return decorator
