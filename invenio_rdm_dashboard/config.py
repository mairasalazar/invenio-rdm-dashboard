# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""Default configuration for invenio-rdm-dashboard."""

#: Routes for the four dashboard tabs.
APP_RDM_USER_DASHBOARD_ROUTES = {
    "uploads": "/me/uploads",
    "communities": "/me/communities",
    "requests": "/me/requests",
    "favourites": "/me/favourites",
}

#: Per-tab overrides (text/order/endpoint) applied on top of the defaults
#: registered in ``ext.py:init_menu``. Keys must already exist there.
USER_DASHBOARD_MENU_OVERRIDES = {}

#: Turns the whole bookmarks feature (REST API, favourites tab, star
#: widgets) on or off, independently of whether this package is
#: installed - lets an instance install invenio-rdm-dashboard for the
#: uploads/communities/requests tabs alone.
BOOKMARKS_ENABLED = True

#: Resource types that can be bookmarked, mapped to the service proxy
#: (as an import path string, resolved lazily) used to resolve display
#: metadata (title, link) for the favourites listing.
BOOKMARKS_RESOURCE_TYPES = {
    "record": "invenio_rdm_records.proxies.current_rdm_records_service",
    "community": "invenio_communities.proxies.current_communities.service",
}

#: Max number of bookmarks a single user may hold, per resource type.
#: Set to ``None`` to disable the limit.
BOOKMARKS_MAX_PER_USER = 2000
