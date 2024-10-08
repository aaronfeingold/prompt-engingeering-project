"""Only messages as a column from PromptResponse

Revision ID: c3fd095f18a2
Revises: ce75154d5de7
Create Date: 2024-07-22 16:11:58.268021

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c3fd095f18a2"
down_revision = "ce75154d5de7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("prompt_response", schema=None) as batch_op:
        batch_op.drop_column("role")
        batch_op.drop_column("content")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("prompt_response", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("content", sa.VARCHAR(), autoincrement=False, nullable=False)
        )
        batch_op.add_column(
            sa.Column("role", sa.VARCHAR(), autoincrement=False, nullable=False)
        )

    # ### end Alembic commands ###
