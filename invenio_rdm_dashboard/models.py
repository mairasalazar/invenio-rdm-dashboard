# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""Database models for invenio-rdm-dashboard."""

import uuid

from invenio_accounts.models import User
from invenio_db import db
from invenio_db.shared import Timestamp
from sqlalchemy import UniqueConstraint
from sqlalchemy_utils.types import UUIDType


class Bookmark(db.Model, Timestamp):
    """A user's bookmark of a record or a community.

    ``resource_type`` mirrors the ``type_id`` used by the entity resolver
    registry (``"record"``, ``"community"``, ...) so the two stay in sync
    if more bookmarkable types are added later.
    """

    __tablename__ = "bookmarks_bookmark"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "resource_type",
            "resource_pid",
            name="uq_bookmarks_bookmark_user_resource",
        ),
    )

    id = db.Column(UUIDType, primary_key=True, default=uuid.uuid4)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(User.id, ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    resource_type = db.Column(db.String(50), nullable=False)

    resource_pid = db.Column(db.String(255), nullable=False)

    user = db.relationship(User)

    @classmethod
    def create(cls, user_id, resource_type, resource_pid):
        """Create and add (but do not commit) a new bookmark."""
        obj = cls(
            id=uuid.uuid4(),
            user_id=user_id,
            resource_type=resource_type,
            resource_pid=resource_pid,
        )
        db.session.add(obj)
        return obj

    @classmethod
    def get(cls, user_id, resource_type, resource_pid):
        """Fetch a single bookmark, or ``None`` if it doesn't exist."""
        return cls.query.filter_by(
            user_id=user_id,
            resource_type=resource_type,
            resource_pid=resource_pid,
        ).one_or_none()

    @classmethod
    def count_for_user(cls, user_id):
        """Count how many bookmarks a user currently holds."""
        return cls.query.filter_by(user_id=user_id).count()

    @classmethod
    def list_for_user(cls, user_id, resource_type=None):
        """Return a query of a user's bookmarks, newest first."""
        query = cls.query.filter_by(user_id=user_id)
        if resource_type is not None:
            query = query.filter_by(resource_type=resource_type)
        return query.order_by(cls.created.desc())
