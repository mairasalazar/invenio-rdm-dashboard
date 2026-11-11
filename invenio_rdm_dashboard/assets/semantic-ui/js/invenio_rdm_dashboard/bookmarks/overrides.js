/*
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: MIT
 *
 * Puts the bookmark star next to the title in the records search-result
 * list, by passing it as the `titleActions` prop that
 * invenio-app-rdm's RecordsResultsListItem already accepts for exactly
 * this purpose - rather than overriding/duplicating that component's
 * title markup wholesale.
 *
 * `RDMRecordResultsListItemWithState` itself is untouched; we only
 * parametrize it with an extra prop and register that as the
 * "ResultsList.item" default, so this is additive, not a replacement of
 * invenio-app-rdm's rendering.
 *
 * This still has to go through react-overridable's overrideStore, since
 * that's the only mechanism in this stack for one package's bundle to
 * reach into another's component tree without a hard import - but
 * unlike a full slot replacement, invenio-app-rdm's own component does
 * all the rendering; this just supplies one prop's value.
 *
 * Also still only works if this script's <script> tag is emitted on the
 * page BEFORE invenio-app-rdm's own search bundle's tag, since that
 * bundle reads overrideStore.getAll() once, at import time. Both tags
 * are now only emitted when BOOKMARKS_ENABLED is true (see
 * records_ui/templates/.../records/search.html).
 */

import { overrideStore, parametrize } from "react-overridable";
import "../../../less/invenio_rdm_dashboard/bookmarks.less";
import { RDMRecordResultsListItemWithState } from "@js/invenio_app_rdm/search/components";
import { RDMRecordResultsListItem as DashboardUploadsResultsListItem } from "../dashboard/uploads_items/RDMRecordResultsListItem";
import { BookmarkStar } from "./BookmarkStar";

const appName = "InvenioAppRdm.Search";

const RDMRecordResultsListItemWithBookmark = parametrize(
  RDMRecordResultsListItemWithState,
  {
    appName,
    titleActions: BookmarkStar,
  }
);

overrideStore.add(`${appName}.ResultsList.item`, RDMRecordResultsListItemWithBookmark);

// Same thing, for the dashboard's "Uploads" tab - a separate component
// tree (it shows draft-specific status labels search.js doesn't need),
// so it has its own appName/registration rather than sharing the one
// above.
const uploadsAppName = "InvenioAppRdm.DashboardUploads";

const DashboardUploadsResultsListItemWithBookmark = parametrize(
  DashboardUploadsResultsListItem,
  {
    titleActions: BookmarkStar,
  }
);

overrideStore.add(
  `${uploadsAppName}.ResultsList.item`,
  DashboardUploadsResultsListItemWithBookmark
);
