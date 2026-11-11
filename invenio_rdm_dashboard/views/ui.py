# SPDX-FileCopyrightText: 2016-2021 CERN.
# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""Dashboard UI and bookmarks REST API blueprints."""

from flask import Blueprint

from ..searchapp import search_app_context
from .dashboard import communities, favourites, requests, uploads


def create_ui_blueprint(app):
    """Register the dashboard's UI blueprint routes on the app."""
    routes = app.config.get("APP_RDM_USER_DASHBOARD_ROUTES")

    blueprint = Blueprint(
        "invenio_rdm_dashboard",
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    blueprint.add_url_rule(routes["uploads"], view_func=uploads)
    blueprint.add_url_rule(routes["communities"], view_func=communities)
    blueprint.add_url_rule(routes["requests"], view_func=requests)

    if app.config["BOOKMARKS_ENABLED"]:
        blueprint.add_url_rule(routes["favourites"], view_func=favourites)

    blueprint.app_context_processor(search_app_context)

    return blueprint


def create_api_blueprint(app):
    """Register the bookmarks REST API blueprint on the app.

    Returns an empty blueprint (no routes) when ``BOOKMARKS_ENABLED`` is
    False, so the feature can be turned off without uninstalling the
    package - e.g. an instance that only wants the uploads/communities/
    requests tabs.
    """
    if not app.config["BOOKMARKS_ENABLED"]:
        return Blueprint("invenio_rdm_dashboard_bookmarks_api", __name__)

    ext = app.extensions["invenio-rdm-dashboard"]
    return ext.bookmarks_resource.as_blueprint()
