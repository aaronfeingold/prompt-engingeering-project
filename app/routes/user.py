from flask import Blueprint, request, jsonify
from app.models import User
from app.database import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required

user_bp = Blueprint("user", __name__)
bcrypt = Bcrypt()


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("roles", "user")  # Default to regular user role
    user = User(username=username, email=email, roles=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


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
