# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""create bookmarks_bookmark.

Revision ID: 9c1f5e8b2a4d
Revises:
Create Date: 2026-11-11 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9c1f5e8b2a4d"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = ("invenio_rdm_dashboard",)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "bookmarks_bookmark",
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("resource_type", sa.String(length=50), nullable=False),
        sa.Column("resource_pid", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["accounts_user.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "resource_type",
            "resource_pid",
            name="uq_bookmarks_bookmark_user_resource",
        ),
    )
    op.create_index(
        op.f("ix_bookmarks_bookmark_user_id"),
        "bookmarks_bookmark",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_bookmarks_bookmark_user_id"), table_name="bookmarks_bookmark"
    )
    op.drop_table("bookmarks_bookmark")
