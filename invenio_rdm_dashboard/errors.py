# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""Errors for invenio-rdm-dashboard."""


class BookmarkNotFoundError(Exception):
    """Raised when a bookmark lookup finds nothing."""


class BookmarkAlreadyExistsError(Exception):
    """Raised when trying to create a bookmark that already exists."""


class InvalidResourceTypeError(Exception):
    """Raised when ``resource_type`` is not one of ``BOOKMARKS_RESOURCE_TYPES``."""

    def __init__(self, resource_type):
        """Initialize."""
        self.resource_type = resource_type
        super().__init__(f"Unknown bookmarkable resource type: '{resource_type}'.")


class BookmarkLimitExceededError(Exception):
    """Raised when a user has reached ``BOOKMARKS_MAX_PER_USER``."""
