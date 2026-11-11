# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""Business logic for creating, removing and listing bookmarks.

Deliberately not built on top of ``invenio-records-resources``'
``RecordService`` framework: bookmarks have no revisions, no search index
and no JSON schema of their own, so a thin service directly over the
``Bookmark`` SQLAlchemy model is simpler and keeps this module's footprint
small.
"""

from importlib import import_module

from flask import current_app
from flask_principal import PermissionDenied
from invenio_db import db
from invenio_pidstore.errors import PersistentIdentifierError

from ..errors import (
    BookmarkAlreadyExistsError,
    BookmarkLimitExceededError,
    BookmarkNotFoundError,
    InvalidResourceTypeError,
)
from ..models import Bookmark


def _import_attr_path(path):
    """Import a dotted path, resolving any number of trailing attributes.

    ``werkzeug.utils.import_string`` only resolves a single attribute past
    the deepest importable module (``module.path:attr``), which breaks for
    something like ``invenio_communities.proxies.current_communities.service``
    - ``current_communities`` is itself an attribute (a ``LocalProxy``), not
    a module, so there's a second attribute (``service``) to resolve on top
    of it. This tries progressively shorter module prefixes until one
    imports, then walks the rest as attributes.
    """
    parts = path.split(".")
    for i in range(len(parts), 0, -1):
        try:
            obj = import_module(".".join(parts[:i]))
        except ImportError:
            continue
        for attr in parts[i:]:
            obj = getattr(obj, attr)
        return obj
    raise ImportError(f"Cannot import '{path}'")


class BookmarksService:
    """Service for managing a user's bookmarks."""

    def _require_authenticated(self, identity):
        if not identity.id:
            raise PermissionDenied()

    def _resource_service(self, resource_type):
        """Resolve the records-resources service backing ``resource_type``."""
        types = current_app.config["BOOKMARKS_RESOURCE_TYPES"]
        path = types.get(resource_type)
        if path is None:
            raise InvalidResourceTypeError(resource_type)
        return _import_attr_path(path)

    def _resolve(self, identity, resource_type, resource_pid):
        """Fetch the target resource, applying *its own* permission policy.

        This both validates that ``resource_pid`` exists and that
        ``identity`` is allowed to see it - we never let someone bookmark
        (or keep bookmarked) something they couldn't otherwise view.
        """
        service = self._resource_service(resource_type)
        return service.read(identity=identity, id_=resource_pid)

    def create(self, identity, resource_type, resource_pid):
        """Bookmark a record or community for the current user."""
        self._require_authenticated(identity)

        # Raises PermissionDeniedError/NotFoundError if not readable.
        self._resolve(identity, resource_type, resource_pid)

        if Bookmark.get(identity.id, resource_type, resource_pid) is not None:
            raise BookmarkAlreadyExistsError()

        max_per_user = current_app.config.get("BOOKMARKS_MAX_PER_USER")
        if max_per_user is not None:
            if Bookmark.count_for_user(identity.id) >= max_per_user:
                raise BookmarkLimitExceededError()

        bookmark = Bookmark.create(identity.id, resource_type, resource_pid)
        db.session.commit()
        return bookmark

    def delete(self, identity, resource_type, resource_pid):
        """Remove a bookmark for the current user."""
        self._require_authenticated(identity)

        bookmark = Bookmark.get(identity.id, resource_type, resource_pid)
        if bookmark is None:
            raise BookmarkNotFoundError()

        db.session.delete(bookmark)
        db.session.commit()

    def is_bookmarked(self, identity, resource_type, resource_pid):
        """Check whether the current user has bookmarked this resource."""
        if not identity.id:
            return False
        return Bookmark.get(identity.id, resource_type, resource_pid) is not None

    #: Supported ``sort`` values for :meth:`list`, mapped to a
    #: ``(sort_key, reverse)`` pair. Bookmarked-date sorting could be done
    #: at the SQL level, but title sorting can't - there's no ``title``
    #: column, it only exists once a bookmark is resolved - so everything
    #: is resolved first and sorted/paginated in Python for one consistent
    #: code path. Fine for a personal bookmarks list; would need
    #: revisiting if this ever needs to scale to large collections.
    SORT_OPTIONS = {
        "bookmarked-desc": (lambda hit: hit["created"], True),
        "bookmarked-asc": (lambda hit: hit["created"], False),
        "title-asc": (lambda hit: hit["title"].lower(), False),
        "title-desc": (lambda hit: hit["title"].lower(), True),
    }

    def list(self, identity, resource_type=None, sort="bookmarked-desc", page=1, size=25):
        """List the current user's bookmarks, resolving display metadata.

        Entries whose target has since become unreadable or was deleted
        are skipped rather than failing the whole listing.
        """
        self._require_authenticated(identity)

        if sort not in self.SORT_OPTIONS:
            sort = "bookmarked-desc"
        sort_key, reverse = self.SORT_OPTIONS[sort]

        query = Bookmark.list_for_user(identity.id, resource_type=resource_type)

        hits = []
        for bookmark in query:
            try:
                resolved = self._resolve(
                    identity, bookmark.resource_type, bookmark.resource_pid
                )
            except (PermissionDenied, PersistentIdentifierError):
                continue
            resolved_dict = resolved.to_dict()
            hits.append(
                {
                    "resource_type": bookmark.resource_type,
                    "resource_pid": bookmark.resource_pid,
                    "created": bookmark.created,
                    "title": resolved_dict.get("metadata", {}).get("title", ""),
                    "resource": resolved_dict,
                }
            )

        hits.sort(key=sort_key, reverse=reverse)

        total = len(hits)
        start = (page - 1) * size
        page_hits = hits[start : start + size]
        for hit in page_hits:
            hit["created"] = hit["created"].isoformat()
            del hit["title"]

        return {"hits": {"hits": page_hits, "total": total}}
