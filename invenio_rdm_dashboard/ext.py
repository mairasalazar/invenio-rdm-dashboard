# SPDX-FileCopyrightText: 2022-2026 CERN.
# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""Invenio-RDM-Dashboard extension.

Merges what used to be two separate things:

- invenio-app-rdm's ``users_ui`` (the logged-in user's "My uploads" /
  "My communities" / "My requests" tabs) - *not* the admin dashboard,
  which stays in invenio-app-rdm's ``administration`` package.
- invenio-bookmarks (now retired): the ``Bookmark`` model, its service
  and REST API, contributed here as a fourth "Favourites" tab.

Registered under ``invenio_base.apps`` / ``invenio_base.api_apps`` - i.e.
only loaded at all if this distribution is installed.
"""

from flask_menu import current_menu
from invenio_i18n import gettext as _

from . import config
from .resources import BookmarksResource, BookmarksResourceConfig
from .services import BookmarksService


class InvenioRDMDashboard(object):
    """Invenio-RDM-Dashboard extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.bookmarks_service = BookmarksService()
        self.bookmarks_resource = BookmarksResource(
            BookmarksResourceConfig(), self.bookmarks_service
        )
        app.extensions["invenio-rdm-dashboard"] = self

    _own_config_keys = {
        "APP_RDM_USER_DASHBOARD_ROUTES",
        "USER_DASHBOARD_MENU_OVERRIDES",
    }

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("BOOKMARKS_") or k in self._own_config_keys:
                app.config.setdefault(k, getattr(config, k))


def finalize_app(app):
    """Finalize app - only meaningful for the UI app (menu registration)."""
    init_menu(app)


def init_menu(app):
    """Register the dashboard's tab bar, including the favourites tab.

    Uses the same ``dashboard`` flask-menu namespace invenio-app-rdm used
    to populate directly in its own ``ext.py`` - the tab bar
    (``header.html``) renders ``current_menu.submenu('dashboard').children``
    generically, so this is a drop-in continuation of that registry, not
    a new mechanism.
    """
    dashboard = current_menu.submenu("dashboard")

    dashboard_menu_config = {
        "uploads": {
            "endpoint": "invenio_rdm_dashboard.uploads",
            "text": _("Uploads"),
            "order": 1,
        },
        "communities": {
            "endpoint": "invenio_rdm_dashboard.communities",
            "text": _("Communities"),
            "order": 2,
        },
        "requests": {
            "endpoint": "invenio_rdm_dashboard.requests",
            "text": _("Requests"),
            "order": 3,
        },
    }

    if app.config["BOOKMARKS_ENABLED"]:
        dashboard_menu_config["favourites"] = {
            "endpoint": "invenio_rdm_dashboard.favourites",
            "text": _("Favourites"),
            "order": 4,
        }

    for submenu_name, submenu_kwargs in app.config[
        "USER_DASHBOARD_MENU_OVERRIDES"
    ].items():
        if submenu_name not in dashboard_menu_config:
            raise ValueError(
                f"attempting to override dashboard's submenu `{submenu_name}`, "
                "but dashboard has no registered submenu of that name"
            )
        dashboard_menu_config[submenu_name].update(submenu_kwargs)

    for submenu_name, submenu_kwargs in dashboard_menu_config.items():
        dashboard.submenu(submenu_name).register(**submenu_kwargs)

    current_menu.submenu("actions.deposit").register(
        endpoint="invenio_rdm_dashboard.uploads",
        text=_("My dashboard"),
        order=1,
    )

    current_menu.submenu("notifications.requests").register(
        "invenio_rdm_dashboard.requests",
        order=1,
    )
