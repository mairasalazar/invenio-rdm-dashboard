# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""REST resource for invenio-rdm-dashboard."""

from flask import g, request
from flask_resources import (
    Resource,
    request_parser,
    resource_requestctx,
    response_handler,
    route,
)

from ..errors import BookmarkNotFoundError
from .config import BookmarkCreateSchema, BookmarkItemViewArgsSchema, BookmarkListArgsSchema

request_view_args = request_parser(BookmarkItemViewArgsSchema, location="view_args")
request_list_args = request_parser(BookmarkListArgsSchema, location="args")


class BookmarksResource(Resource):
    """Resource for a user's bookmarks."""

    def __init__(self, config, service):
        """Initialize the resource with its backing service."""
        super().__init__(config)
        self.service = service

    def create_url_rules(self):
        """Create the URL rules for the bookmarks resource."""
        routes = self.config.routes
        return [
            route("GET", routes["list"], self.search),
            route("POST", routes["list"], self.create),
            route("GET", routes["item"], self.read),
            route("DELETE", routes["item"], self.delete),
        ]

    @request_list_args
    @response_handler()
    def search(self):
        """List the current user's bookmarks."""
        args = resource_requestctx.args
        result = self.service.list(
            identity=g.identity,
            resource_type=args["resource_type"],
            sort=args["sort"],
            page=args["page"],
            size=args["size"],
        )
        return result, 200

    @response_handler()
    def create(self):
        """Bookmark a record or community."""
        data = BookmarkCreateSchema().load(request.get_json())
        bookmark = self.service.create(
            identity=g.identity,
            resource_type=data["resource_type"],
            resource_pid=data["resource_pid"],
        )
        return {
            "resource_type": bookmark.resource_type,
            "resource_pid": bookmark.resource_pid,
            "created": bookmark.created.isoformat(),
        }, 201

    @request_view_args
    @response_handler()
    def read(self):
        """Check whether the current user has bookmarked this resource."""
        args = resource_requestctx.view_args
        bookmarked = self.service.is_bookmarked(
            identity=g.identity,
            resource_type=args["resource_type"],
            resource_pid=args["resource_pid"],
        )
        if not bookmarked:
            raise BookmarkNotFoundError()
        return {"bookmarked": True}, 200

    @request_view_args
    def delete(self):
        """Remove a bookmark."""
        args = resource_requestctx.view_args
        self.service.delete(
            identity=g.identity,
            resource_type=args["resource_type"],
            resource_pid=args["resource_pid"],
        )
        return "", 204
