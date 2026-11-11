# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""Blueprints for invenio-rdm-dashboard."""

from .ui import create_api_blueprint, create_ui_blueprint

__all__ = ("create_api_blueprint", "create_ui_blueprint")
