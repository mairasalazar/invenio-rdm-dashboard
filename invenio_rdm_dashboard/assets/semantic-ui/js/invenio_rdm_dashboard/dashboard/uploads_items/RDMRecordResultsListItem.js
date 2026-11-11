/*
 * SPDX-FileCopyrightText: 2020-2022 CERN.
 * SPDX-FileCopyrightText: 2020-2021 Northwestern University.
 * SPDX-FileCopyrightText: 2021 Graz University of Technology.
 * SPDX-FileCopyrightText: 2021 New York University.
 * SPDX-FileCopyrightText: 2024 KTH Royal Institute of Technology.
 * SPDX-License-Identifier: MIT
 *
 * Split out of ../uploads.js: that file calls `createSearchAppInit` as a
 * side effect at import time, so importing anything from it elsewhere (as
 * bookmarks/overrides.js needs to, to parametrize this component with the
 * bookmark star) would boot the Uploads search app a second time - with
 * ES module imports executing before the importing module's own top-level
 * code, that premature boot happens before the override is even
 * registered, so the real mount never gets it. This module has no such
 * side effect, so it's safe to import from anywhere.
 */

import { i18next } from "@translations/invenio_app_rdm/i18next";
import _get from "lodash/get";
import React from "react";
import PropTypes from "prop-types";
import { ComputerTabletUploadsItem } from "./ComputerTabletUploadsItem";
import { MobileUploadsItem } from "./MobileUploadsItem";

export const statuses = {
  in_review: { color: "warning", title: i18next.t("In review") },
  declined: { color: "negative", title: i18next.t("Declined") },
  expired: { color: "expired", title: i18next.t("Expired") },
  draft_with_review: { color: "neutral", title: i18next.t("Draft") },
  draft: { color: "neutral", title: i18next.t("Draft") },
  new_version_draft: { color: "neutral", title: i18next.t("New version draft") },
};

export const RDMRecordResultsListItem = ({ result, titleActions }) => {
  const viewDraft = () => {
    // The upload view is responsible to redirect the user to the upload form or
    // the preview page depending on the permissions they have.
    window.location = `/uploads/${result.id}`;
  };

  const isPublished = result.is_published;
  const access = {
    accessStatusId: _get(result, "ui.access_status.id", i18next.t("open")),
    accessStatus: _get(result, "ui.access_status.title_l10n", i18next.t("Open")),
    accessStatusIcon: _get(result, "ui.access_status.icon", i18next.t("unlock")),
  };
  const uiMetadata = {
    descriptionStripped: _get(
      result,
      "ui.description_stripped",
      i18next.t("No description")
    ),
    title: _get(result, "metadata.title", i18next.t("No title")),
    creators: _get(result, "ui.creators.creators", []),
    subjects: _get(result, "ui.subjects", []),
    publicationDate: _get(
      result,
      "ui.publication_date_l10n_long",
      i18next.t("No publication date found.")
    ),
    resourceType: _get(
      result,
      "ui.resource_type.title_l10n",
      i18next.t("No resource type")
    ),
    createdDate: result.ui?.created_date_l10n_long,
    version: result.ui?.version ?? "",
    isPublished: isPublished,
    viewLink: isPublished ? `/records/${result.id}` : `/uploads/${result.id}`,
    publishingInformation: _get(result, "ui.publishing_information.journal", ""),
  };

  return (
    <>
      <ComputerTabletUploadsItem
        result={result}
        viewDraft={viewDraft}
        statuses={statuses}
        access={access}
        uiMetadata={uiMetadata}
        titleActions={titleActions}
      />
      <MobileUploadsItem
        result={result}
        viewDraft={viewDraft}
        statuses={statuses}
        access={access}
        uiMetadata={uiMetadata}
        titleActions={titleActions}
      />
    </>
  );
};

RDMRecordResultsListItem.propTypes = {
  result: PropTypes.object.isRequired,
  titleActions: PropTypes.elementType,
};

RDMRecordResultsListItem.defaultProps = {
  titleActions: null,
};
