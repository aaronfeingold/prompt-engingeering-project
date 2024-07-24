"""columns for the prompt response content and role

Revision ID: a924af2005c1
Revises: 98ec2b047e77
Create Date: 2024-07-15 13:56:41.692690

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a924af2005c1"
down_revision = "98ec2b047e77"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("prompt_response", schema=None) as batch_op:
        batch_op.add_column(sa.Column("content", sa.String(), nullable=False))
        batch_op.add_column(sa.Column("role", sa.String(), nullable=False))
        batch_op.drop_column("response")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("prompt_response", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("response", sa.VARCHAR(), autoincrement=False, nullable=False)
        )
        batch_op.drop_column("role")
        batch_op.drop_column("content")

    # ### end Alembic commands ###
