from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
import openai
from app.services import PromptResponseService
from app.models import User, Team


@jwt_required()
def create_new_prompt_response(request):
    prompt_messages = request.json.get("prompt_messages")
    team_id = request.json.get("team_id")
    if not prompt_messages:
        return jsonify({"error": "A Message is required"}), 400
    try:
        # Extract user information from the JWT token
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get team information
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"error": "Team not found"}), 404
        response_data = PromptResponseService.create_new_prompt_response(
            prompt_messages
        )

        return jsonify(response_data), 201
    except openai.RateLimitError as e:
        return (
            jsonify(
                {"error": f"API rate limit exceeded: {e}. Please try again later."}
            ),
            429,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An error occurred while processing your request",
                    "details": e,
                }
            ),
            500,
        )


def query_prompt_responses(request):
    try:
        # parse the args from the request
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        sort_by = request.args.get(
            "sort_by", "created_at"
        )  # Default sort by created_at
        sort_order = request.args.get("sort_order", "asc")

        if sort_by not in ["response_time", "created_at"]:
            return jsonify({"error": "Invalid sort_by parameter"}), 400

        if sort_order not in ["asc", "desc"]:
            return jsonify({"error": "Invalid sort_order parameter"}), 400

        return (
            jsonify(
                PromptResponseService.query_prompt_responses(
                    page, per_page, sort_by, sort_order
                )
            ),
            200,
        )
    except ValueError:
        return jsonify({"error": "Page and per_page parameters must be integers"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
