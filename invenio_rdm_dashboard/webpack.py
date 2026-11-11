# SPDX-FileCopyrightText: 2019-2025 CERN.
# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT

"""JS/CSS Webpack bundles for invenio-rdm-dashboard."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                # Moved from invenio-app-rdm's theme bundle (user_dashboard/*).
                "invenio-rdm-dashboard-uploads": "./js/invenio_rdm_dashboard/dashboard/uploads.js",
                "invenio-rdm-dashboard-communities": "./js/invenio_rdm_dashboard/dashboard/communities.js",
                "invenio-rdm-dashboard-requests": "./js/invenio_rdm_dashboard/dashboard/requests.js",
                # From the now-retired invenio-bookmarks.
                "invenio-rdm-dashboard-favourites": "./js/invenio_rdm_dashboard/favourites.js",
                # Supplies the bookmark star as the `titleActions` prop
                # RecordsResultsListItem already accepts for this purpose -
                # must load on the page before invenio-app-rdm's own
                # search.js bundle. Both are only emitted when
                # BOOKMARKS_ENABLED is true (see search.html).
                "invenio-rdm-dashboard-bookmark-overrides": "./js/invenio_rdm_dashboard/bookmarks/overrides.js",
                # Mounts the bookmark star next to the title on the record
                # landing page - see invenio-app-rdm's detail.html.
                "invenio-rdm-dashboard-record-star": "./js/invenio_rdm_dashboard/bookmarks/recordStar.js",
                # Same two, for communities - see invenio-communities'
                # search.html and details/base.html.
                "invenio-rdm-dashboard-community-bookmark-overrides": "./js/invenio_rdm_dashboard/bookmarks/communityOverrides.js",
                "invenio-rdm-dashboard-community-star": "./js/invenio_rdm_dashboard/bookmarks/communityStar.js",
            },
            dependencies={
                "@babel/runtime": "^7.9.0",
                "react-overridable": "^1.0.0",
            },
        ),
    },
)
