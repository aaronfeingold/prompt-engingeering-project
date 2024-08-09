"""change back population of User to Team relationship

Revision ID: cdba6c51ae4d
Revises: 071a6546fc40
Create Date: 2024-08-09 13:37:22.102671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cdba6c51ae4d"
down_revision = "071a6546fc40"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "regular_budget",
            existing_type=sa.INTEGER(),
            type_=sa.Float(),
            existing_nullable=False,
            existing_server_default=sa.text("150.00"),
        )
        batch_op.alter_column(
            "temporary_budget",
            existing_type=sa.INTEGER(),
            type_=sa.Float(),
            existing_nullable=True,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.alter_column(
            "temporary_budget",
            existing_type=sa.Float(),
            type_=sa.INTEGER(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "regular_budget",
            existing_type=sa.Float(),
            type_=sa.INTEGER(),
            existing_nullable=False,
            existing_server_default=sa.text("150.00"),
        )

    # ### end Alembic commands ###
