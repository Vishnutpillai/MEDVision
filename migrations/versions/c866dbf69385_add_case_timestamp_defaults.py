"""add case timestamp defaults

Revision ID: c866dbf69385
Revises: ed8bbeb87992
Create Date: 2026-09-24 18:46:49.932626

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c866dbf69385"
down_revision = "ed8bbeb87992"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("cases", schema=None) as batch_op:

        batch_op.alter_column(
            "status",
            existing_type=sa.VARCHAR(length=30),
            type_=sa.String(length=50),
            existing_nullable=False,
        )

        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            existing_nullable=False,
        )

        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            existing_nullable=False,
        )

        batch_op.drop_index(
            batch_op.f("ix_cases_user_id")
        )

        batch_op.drop_constraint(
            batch_op.f("cases_user_id_fkey"),
            type_="foreignkey",
        )

        batch_op.create_foreign_key(
            None,
            "users",
            ["user_id"],
            ["id"],
        )


def downgrade():

    with op.batch_alter_table("cases", schema=None) as batch_op:

        batch_op.drop_constraint(
            None,
            type_="foreignkey",
        )

        batch_op.create_foreign_key(
            batch_op.f("cases_user_id_fkey"),
            "users",
            ["user_id"],
            ["id"],
            ondelete="CASCADE",
        )

        batch_op.create_index(
            batch_op.f("ix_cases_user_id"),
            ["user_id"],
            unique=False,
        )

        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(timezone=True),
            server_default=None,
            existing_nullable=False,
        )

        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(timezone=True),
            server_default=None,
            existing_nullable=False,
        )

        batch_op.alter_column(
            "status",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=30),
            existing_nullable=False,
        )