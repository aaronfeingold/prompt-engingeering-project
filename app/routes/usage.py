from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.decorators import role_required, validate_schema, PromptResponseSchema
from app.models.user import RoleEnum

usage_bp = Blueprint("usage", __name__)

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


@usage_bp.route("/user", methods=["GET"])
@jwt_required()
@role_required([RoleEnum.USER, RoleEnum.ADMIN])
@validate_schema(PromptResponseSchema())
def post_prompt():
    import pandas as pd
    from sqlalchemy import create_engine

    data = request.get_json()
    user = data.get("user")
    # Database connection
    DATABASE_URL = "postgresql://username:password@localhost/dbname"
    engine = create_engine(DATABASE_URL)

    # Fetch data
    query = """
    SELECT
        pr.id AS prompt_response_id,
        pr.user_id,
        pr.team_id,
        pr.created_at,
        ou.prompt_tokens,
        ou.completion_tokens,
        ou.model_name
    FROM
        prompt_response pr
    JOIN
        openai_usage ou ON pr.id = ou.prompt_response_id;
    """
    df = pd.read_sql(query, engine)

    # Calculate cost per prompt
    def calculate_cost(row):
        model = row["model_name"]
        input_tokens = row["prompt_tokens"]
        output_tokens = row["completion_tokens"]

        if model in MODEL_PRICING:
            pricing = MODEL_PRICING[model]
            input_cost = input_tokens * pricing.get("input", 0)
            output_cost = output_tokens * pricing.get("output", 0)
            total_cost = input_cost + output_cost
            return total_cost
        else:
            # Handle cases where the model is not in the pricing dictionary
            return 0.0

    df["cost"] = df.apply(calculate_cost, axis=1)
