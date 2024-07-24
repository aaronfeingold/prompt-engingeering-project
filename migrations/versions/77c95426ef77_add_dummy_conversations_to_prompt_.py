"""Add dummy conversations to prompt_responses with them

Revision ID: 77c95426ef77
Revises: a924af2005c1
Create Date: 2024-07-22 15:36:56.400482

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "77c95426ef77"
down_revision = "a924af2005c1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "conversation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("prompt_response", schema=None) as batch_op:
        batch_op.add_column(sa.Column("conversation_id", sa.Integer(), nullable=True))
        batch_op.alter_column(
            "prompt",
            existing_type=sa.VARCHAR(),
            type_=sa.Text(),
            existing_nullable=False,
        )
        batch_op.create_foreign_key(None, "conversation", ["conversation_id"], ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("prompt_response", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.alter_column(
            "prompt",
            existing_type=sa.Text(),
            type_=sa.VARCHAR(),
            existing_nullable=False,
        )
        batch_op.drop_column("conversation_id")

    op.drop_table("conversation")
    # ### end Alembic commands ###
