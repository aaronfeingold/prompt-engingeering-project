from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models import User


def role_required(required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not any(role in user.role for role in required_roles):
                return (
                    jsonify({"message": "Access forbidden: insufficient permissions"}),
                    403,
                )
            return f(*args, **kwargs)

        return decorated_function

    return decorator
