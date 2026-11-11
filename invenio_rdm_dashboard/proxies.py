# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""Proxies to the invenio-rdm-dashboard extension and its bookmarks service."""

from flask import current_app
from werkzeug.local import LocalProxy

current_dashboard = LocalProxy(
    lambda: current_app.extensions["invenio-rdm-dashboard"]
)

current_bookmarks_service = LocalProxy(
    lambda: current_app.extensions["invenio-rdm-dashboard"].bookmarks_service
)
