# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""REST resource configuration for invenio-rdm-dashboard."""

import marshmallow as ma
from flask_principal import PermissionDenied
from flask_resources import (
    HTTPJSONException,
    JSONSerializer,
    MultiDictSchema,
    ResourceConfig,
    ResponseHandler,
    create_error_handler,
)
from invenio_pidstore.errors import PersistentIdentifierError

from ..errors import (
    BookmarkAlreadyExistsError,
    BookmarkLimitExceededError,
    BookmarkNotFoundError,
    InvalidResourceTypeError,
)


class BookmarkItemViewArgsSchema(MultiDictSchema):
    """View args for a single bookmark (``/me/bookmarks/<type>/<pid>``)."""

    resource_type = ma.fields.String(required=True)
    resource_pid = ma.fields.String(required=True)


class BookmarkListArgsSchema(MultiDictSchema):
    """Query string args for listing bookmarks."""

    resource_type = ma.fields.String(load_default=None)
    sort = ma.fields.String(load_default="bookmarked-desc")
    page = ma.fields.Integer(load_default=1)
    size = ma.fields.Integer(load_default=25)


class BookmarkCreateSchema(ma.Schema):
    """Body schema for creating a bookmark."""

    resource_type = ma.fields.String(required=True)
    resource_pid = ma.fields.String(required=True)


class BookmarksResourceConfig(ResourceConfig):
    """Configuration for :class:`~invenio_rdm_dashboard.resources.resource.BookmarksResource`."""

    blueprint_name = "bookmarks"
    url_prefix = "/me/bookmarks"

    routes = {
        "list": "",
        "item": "/<resource_type>/<resource_pid>",
    }

    response_handlers = {
        "application/json": ResponseHandler(JSONSerializer()),
    }

    error_handlers = {
        PermissionDenied: create_error_handler(HTTPJSONException(code=403)),
        PersistentIdentifierError: create_error_handler(HTTPJSONException(code=404)),
        BookmarkNotFoundError: create_error_handler(HTTPJSONException(code=404)),
        BookmarkAlreadyExistsError: create_error_handler(HTTPJSONException(code=409)),
        BookmarkLimitExceededError: create_error_handler(HTTPJSONException(code=429)),
        InvalidResourceTypeError: create_error_handler(HTTPJSONException(code=400)),
    }
