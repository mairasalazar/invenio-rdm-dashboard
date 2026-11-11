# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""REST resources for invenio-rdm-dashboard."""

from .config import BookmarksResourceConfig
from .resource import BookmarksResource

__all__ = ("BookmarksResource", "BookmarksResourceConfig")
