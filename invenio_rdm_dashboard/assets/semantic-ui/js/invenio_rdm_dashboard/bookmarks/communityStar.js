/*
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: MIT
 *
 * Mounts the bookmark star next to the title on the community profile
 * page. See invenio-communities' details/header.html for the mount
 * points - there are two (desktop + mobile layouts), both sharing the
 * `invenio-rdm-dashboard-community-star` class rather than an id, since
 * the title markup is rendered twice on that page.
 */

import React from "react";
import ReactDOM from "react-dom";
import { BookmarkStar } from "./BookmarkStar";

document.querySelectorAll(".invenio-rdm-dashboard-community-star").forEach((root) => {
  const communityId = root.dataset.communityId;
  ReactDOM.render(
    <BookmarkStar result={{ id: communityId }} resourceType="community" />,
    root
  );
});
