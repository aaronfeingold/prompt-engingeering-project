"""Add new column called responses

Revision ID: 4ffd784181ce
Revises: ee18938c5ff9
Create Date: 2024-07-23 16:18:40.109639

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import table, column, select, bindparam
import json

# revision identifiers, used by Alembic.
revision = "4ffd784181ce"
down_revision = "ee18938c5ff9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("prompt_response", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "responses", postgresql.JSONB(astext_type=sa.Text()), nullable=True
            )
        )

    # ### end Alembic commands ###
    # Use SQLAlchemy's table and column to access and update the data
    prompt_response = table(
        "prompt_response",
        column("id", sa.Integer),
        column("messages", sa.String),
        column("responses", postgresql.JSONB),
    )

    # Bind the connection
    conn = op.get_bind()

    # use a batch approach to update the data
    def migrate_messages_data(batch_size=1000):
        offset = 0
        while True:
            results = (
                conn.execute(
                    select(prompt_response.c.id, prompt_response.c.messages)
                    .limit(batch_size)
                    .offset(offset)
                )
                .mappings()
                .fetchall()
            )

            if not results:
                break

            updates = []
            for row in results:
                try:
                    # try to load the json
                    json_messages = json.loads(row["messages"])
                except json.JSONDecodeError as e:
                    # if string cannot be loaded as json, throw an error for now
                    raise RuntimeError(f"Failed to load JSON data: {e}")

                updates.append(
                    {
                        "b_id": row["id"],
                        "responses": json_messages,
                    }
                )
            if updates:
                conn.execute(
                    prompt_response.update()
                    .where(prompt_response.c.id == bindparam("b_id"))
                    .values(responses=bindparam("responses")),
                    updates,
                )

            offset += batch_size

    migrate_messages_data()

    # After data migration, set the 'responses' column to not nullable
    op.alter_column("prompt_response", "responses", nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("prompt_response", schema=None) as batch_op:
        batch_op.drop_column("responses")

    # ### end Alembic commands ###