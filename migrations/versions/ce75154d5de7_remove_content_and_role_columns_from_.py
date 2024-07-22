"""Remove content and role columns from PromptResponse

Revision ID: ce75154d5de7
Revises: 77c95426ef77
Create Date: 2024-07-22 15:52:41.718251

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column, select
import json


# revision identifiers, used by Alembic.
revision = "ce75154d5de7"
down_revision = "77c95426ef77"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("prompt_response", schema=None) as batch_op:
        batch_op.add_column(sa.Column("messages", sa.Text(), nullable=True))

    # ### end Alembic commands ###
    # Use SQLAlchemy's table and column to access and update the data
    prompt_response = table(
        "prompt_response",
        column("id", sa.Integer),
        column("content", sa.String),
        column("role", sa.String),
        column("messages", sa.Text),
    )

    # Bind the connection
    conn = op.get_bind()

    # Fetch and update each row
    results = conn.execute(select(prompt_response)).mappings().fetchall()
    for row in results:
        messages = json.dumps({"content": row["content"], "role": row["role"]})
        conn.execute(
            prompt_response.update()
            .where(prompt_response.c.id == row["id"])
            .values(messages=messages)
        )

    # After data migration, set the 'messages' column to not nullable
    op.alter_column("prompt_response", "messages", nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("prompt_response", schema=None) as batch_op:
        batch_op.drop_column("messages")

    # ### end Alembic commands ###