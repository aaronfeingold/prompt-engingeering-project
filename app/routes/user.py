from flask import Blueprint, request, jsonify
from app.models import User
from app.models.user import RoleEnum
from app.database import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint("user", __name__)
bcrypt = Bcrypt()


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Validate input data
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", RoleEnum.USER.name)  # Default to regular user role
    # TODO: handle two-factor authentication setup
    # TODO: handle OAuth registration

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    # Check if user already exists
    if (
        User.query.filter_by(username=username).first()
        or User.query.filter_by(email=email).first()
    ):
        return (
            jsonify({"error": "User with this username or email already exists"}),
            409,
        )

    try:
        # Create new user
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        # Only set regular_budget if provided, will default to 150.00 otherwise
        if "regular_budget" in data:
            user.regular_budget = data["regular_budget"]
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": f"Database integrity error: {e}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    # users login with email and password
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401


@user_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # JWT tokens are stateless, so we can't invalidate them server-side.
    # Implement token blacklisting if needed.
    return jsonify({"message": "User logged out successfully"}), 200
