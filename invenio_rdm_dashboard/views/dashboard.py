# SPDX-FileCopyrightText: 2022 CERN.
# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""RDM User dashboard views."""

from flask import g, render_template
from flask_login import current_user, login_required
from invenio_app_rdm.records_ui.views.deposits import get_search_url
from invenio_communities.proxies import current_communities
from invenio_users_resources.proxies import current_user_resources


def _user_avatar():
    return current_user_resources.users_service.links_item_tpl.expand(
        g.identity, current_user
    )["avatar"]


@login_required
def uploads():
    """Display user dashboard page."""
    return render_template(
        "invenio_rdm_dashboard/uploads.html",
        searchbar_config=dict(searchUrl=get_search_url()),
        user_avatar=_user_avatar(),
    )


@login_required
def requests():
    """Display user dashboard page."""
    return render_template(
        "invenio_rdm_dashboard/requests.html",
        searchbar_config=dict(searchUrl=get_search_url()),
        user_avatar=_user_avatar(),
    )


@login_required
def communities():
    """Display user dashboard page."""
    can_create_community = current_communities.service.check_permission(
        g.identity, "create"
    )
    return render_template(
        "invenio_rdm_dashboard/communities.html",
        searchbar_config=dict(searchUrl=get_search_url()),
        user_avatar=_user_avatar(),
        can_create_community=can_create_community,
    )


@login_required
def favourites():
    """Display the user's bookmarked records and communities."""
    return render_template(
        "invenio_rdm_dashboard/favourites.html",
        user_avatar=_user_avatar(),
    )
