from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators import role_required, validate_schema, PromptResponseSchema
from app.models.user import RoleEnum
from app.database import db
from app.models import PromptResponse, OpenAIUsage
import pandas as pd

usage_bp = Blueprint("usage", __name__)

# TODO: Consider the pricing models of other providers
# Pricing per 1,000,000 tokens in USD
# TODO: Scrape for this data routinely from OpenAI's pricing page or API
# Probably only changes 3-4x per year
MODEL_PRICING = {
    "gpt-4o": {"input": 2.50 / 1000000, "output": 10.00 / 1000000},
    "gpt-4o-mini": {"input": 0.150 / 1000000, "output": 0.600 / 1000000},
    "gpt-4o-audio-preview": {
        "text_input": 2.50 / 1000000,
        "text_output": 10.00 / 1000000,
        "audio_input": 40.00 / 1000000,
        "audio_output": 80.00 / 1000000,
    },
    # Add other models as needed
}


@usage_bp.route("/user/", methods=["GET"])
@jwt_required()
@role_required([RoleEnum.USER, RoleEnum.ADMIN])
@validate_schema(PromptResponseSchema())
def get_usage_user():
    """
    Fetches the AI usage statistics for the logged-in user, including cost calculations.
    """
    user_id = get_jwt_identity()
    # Fetch user's usage data
    results = (
        db.query(
            PromptResponse.id.label("prompt_response_id"),
            PromptResponse.user_id,
            PromptResponse.team_id,
            PromptResponse.created_at,
            OpenAIUsage.prompt_tokens,
            OpenAIUsage.completion_tokens,
            OpenAIUsage.model_name,
        )
        .join(OpenAIUsage, PromptResponse.id == OpenAIUsage.prompt_response_id)
        .filter(PromptResponse.user_id == user_id)
        .all()
    )

    if not results:
        raise user_id(status_code=404, detail="No usage data found for user.")

    # Convert to Pandas DataFrame
    df = pd.DataFrame(
        results,
        columns=[
            "prompt_response_id",
            "user_id",
            "team_id",
            "created_at",
            "prompt_tokens",
            "completion_tokens",
            "model_name",
        ],
    )

    # Calculate cost per prompt
    def calculate_cost(row):
        model = row["model_name"]
        input_tokens = row["prompt_tokens"]
        output_tokens = row["completion_tokens"]

        if model in MODEL_PRICING:
            pricing = MODEL_PRICING[model]
            input_cost = input_tokens * pricing.get("input", 0)
            output_cost = output_tokens * pricing.get("output", 0)
            return input_cost + output_cost
        return 0.0

    df["cost"] = df.apply(calculate_cost, axis=1)

    # Aggregate total usage cost
    total_cost = df["cost"].sum()
    total_prompt_tokens = df["prompt_tokens"].sum()
    total_completion_tokens = df["completion_tokens"].sum()

    return {
        "user_id": user_id,
        "total_cost": total_cost,
        "total_prompt_tokens": total_prompt_tokens,
        "total_completion_tokens": total_completion_tokens,
        "usage_breakdown": df.to_dict(orient="records"),
    }
