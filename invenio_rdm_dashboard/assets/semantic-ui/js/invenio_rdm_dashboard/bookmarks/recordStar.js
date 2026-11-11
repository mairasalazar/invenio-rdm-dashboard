/*
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: MIT
 *
 * Mounts the bookmark star next to the title on the record landing page.
 * See invenio-app-rdm's detail.html for the mount point
 * (#invenio-rdm-dashboard-record-star) and
 * records_ui/views/filters.py:optional_webpack_tag for why the script
 * tag that loads this bundle is guarded rather than a plain
 * {{ webpack[...] }} lookup.
 */

import React from "react";
import ReactDOM from "react-dom";
import { BookmarkStar } from "./BookmarkStar";

const root = document.getElementById("invenio-rdm-dashboard-record-star");
if (root) {
  const recordId = root.dataset.recordId;
  ReactDOM.render(
    <BookmarkStar result={{ id: recordId }} resourceType="record" />,
    root
  );
}
