"""User and Team Tables with Associations to prompt response and usage

Revision ID: c5bf0fbb8979
Revises: 897ea17c354c
Create Date: 2024-07-25 16:27:02.715186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c5bf0fbb8979"
down_revision = "897ea17c354c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_size", sa.Integer(), nullable=True),
        sa.Column("regular_budget", sa.Integer(), nullable=True),
        sa.Column("temporary_budget", sa.Integer(), nullable=True),
        sa.Column("temporary_budget_expiration", sa.DateTime(), nullable=True),
        sa.Column("team_size_limit", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=128), nullable=False),
        sa.Column("two_fa_setup", sa.Boolean(), nullable=True),
        sa.Column("two_fa_secret", sa.String(length=32), nullable=True),
        sa.Column("two_fa_backup_codes", sa.ARRAY(sa.String()), nullable=True),
        sa.Column(
            "role",
            sa.Enum("USER", "ADMIN", "SUPER_ADMIN", name="roleenum"),
            nullable=False,
        ),
        sa.Column("regular_budget", sa.Integer(), nullable=True),
        sa.Column("team_budgeted", sa.Boolean(), nullable=True),
        sa.Column("temporary_budget", sa.Integer(), nullable=True),
        sa.Column("temporary_budget_expiration", sa.DateTime(), nullable=True),
        sa.Column("date_created", sa.DateTime(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "team_leaders",
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("team_id", "user_id"),
    )
    op.create_table(
        "teammates",
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("team_id", "user_id"),
    )
    with op.batch_alter_table("openai_usage", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("team_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, "teams", ["team_id"], ["id"])
        batch_op.create_foreign_key(None, "users", ["user_id"], ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("openai_usage", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("team_id")
        batch_op.drop_column("user_id")

    op.drop_table("teammates")
    op.drop_table("team_leaders")
    op.drop_table("users")
    op.drop_table("teams")
    # ### end Alembic commands ###