/*
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: MIT
 *
 * Puts the bookmark star next to the title in the communities
 * search-result list, the same way bookmarks/overrides.js does for
 * records: by passing it as the `titleActions` prop that
 * invenio-communities' CommunityItem already accepts for exactly this
 * purpose, rather than overriding/duplicating that component.
 *
 * Only works if this script's <script> tag is emitted on the page
 * BEFORE invenio-communities' own search bundle's tag - see
 * invenio_communities/templates/.../communities/search.html.
 */

import React from "react";
import { overrideStore, parametrize } from "react-overridable";
import "../../../less/invenio_rdm_dashboard/bookmarks.less";
import { CommunityItem } from "@js/invenio_communities/community";
import { BookmarkStar } from "./BookmarkStar";

export const CommunityBookmarkStar = (props) => (
  <BookmarkStar {...props} resourceType="community" />
);

const appName = "InvenioCommunities.Search";

const CommunityItemWithBookmark = parametrize(CommunityItem, {
  titleActions: CommunityBookmarkStar,
});

overrideStore.add(`${appName}.ResultsList.item`, CommunityItemWithBookmark);
