from flask import jsonify
from flask_jwt_extended import get_jwt_identity
import openai
from app.services import PromptResponseService, UserService, TeamService
from app.models import User, Team


def create_new_prompt_response(request):
    validated_data = request.validated_data
    prompt_messages, team_id, model, max_tokens = (
        validated_data["prompt_messages"],
        validated_data["team_id"],
        validated_data["model"],
        validated_data["max_tokens"],
    )
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
            # TODO: get try to get the user's team if not supplied in request
            return jsonify({"error": "Team not found"}), 404
        return (
            jsonify(
                PromptResponseService.create_new_prompt_response(
                    prompt_messages, user, team, model, max_tokens, conversation_id=None
                )
            ),
            201,
        )

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
    # get the username
    user_identity = get_jwt_identity()
    # if there is a list of users in the request, use that instead
    # but first check if the user is an admin or a team leader
    # if team leader, only allow them to query their team's responses
    user_profile = UserService.get_user_profile(user_identity)
    usernames = [user_profile["username"]]
    if user_profile["role"] == "team_leader":
        user_list = request.args.getlist("users")
        if user_list:
            team_members = []
            for team_id in user_profile["leading_teams"]:
                team_members.extend(TeamService.get_team_members(team_id))
            usernames = list(set(user_list) & set(team_members))
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
                    page, per_page, sort_by, sort_order, usernames=usernames
                )
            ),
            200,
        )
    except ValueError:
        return jsonify({"error": "Page and per_page parameters must be integers"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
