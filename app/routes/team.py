from flask import Blueprint, request, jsonify
from app.models import Team
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint("user", __name__)
bcrypt = Bcrypt()


@user_bp.route("/", methods=["POST"])
def register():
    data = request.get_json()

    # Validate input data
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    team_name = data.get("team_name")
    team_leader_ids = data.get("team_leader_ids")
    team_size_limit = data.get("team_size_limit")

    if not team_name:
        return jsonify({"error": "Username, email, and password are required"}), 400

    # Check if user already exists
    if Team.query.filter_by(team_name=team_name).first():
        return (
            jsonify({"error": f"Team with this team name {team_name}already exists"}),
            409,
        )

    try:
        # Create new user
        user = Team(
            team_name=team_name,
            team_leaders=team_leaders,
            team_size_limit=team_size_limit,
        )
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


@user_bp.route("/usage", methods=["POST"])
@jwt_required()
def logout():
    # JWT tokens are stateless, so we can't invalidate them server-side.
    # Implement token blacklisting if needed.
    return jsonify({"message": "User logged out successfully"}), 200
