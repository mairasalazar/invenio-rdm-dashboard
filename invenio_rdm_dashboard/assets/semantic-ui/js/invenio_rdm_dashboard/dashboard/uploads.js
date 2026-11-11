/*
 * SPDX-FileCopyrightText: 2020-2022 CERN.
 * SPDX-FileCopyrightText: 2020-2021 Northwestern University.
 * SPDX-FileCopyrightText: 2021 Graz University of Technology.
 * SPDX-FileCopyrightText: 2021 New York University.
 * SPDX-FileCopyrightText: 2024 KTH Royal Institute of Technology.
 * SPDX-License-Identifier: MIT
 */

import { i18next } from "@translations/invenio_app_rdm/i18next";
import _get from "lodash/get";
import _truncate from "lodash/truncate";
import React from "react";
import { Button, Card, Divider, Header, Segment } from "semantic-ui-react";
import { parametrize, overrideStore } from "react-overridable";
import {
  RDMCountComponent,
  RDMEmptyResults as RDMNoSearchResults,
  RDMRecordSearchBarElement,
  RDMToggleComponent,
} from "@js/invenio_app_rdm/search/components";
import { DashboardResultView, DashboardSearchLayoutHOC } from "./base";
import { createSearchAppInit } from "@js/invenio_search_ui";
import { RDMRecordResultsListItem } from "./uploads_items/RDMRecordResultsListItem";
import PropTypes from "prop-types";
import {
  ContribSearchAppFacets,
  ContribBucketAggregationElement,
  ContribBucketAggregationValuesElement,
  ContribRangeFacetElement,
} from "@js/invenio_search_ui/components";

export { RDMRecordResultsListItem };

// FIXME: Keeping ResultsGrid.item and SearchBar.element because otherwise
// these components in RDM result broken.

export const RDMRecordResultsGridItem = ({ result, index }) => {
  const descriptionStripped = _get(
    result,
    "ui.description_stripped",
    i18next.t("No description")
  );
  return (
    <Card fluid key={index} href={`/records/${result.id}`}>
      <Card.Content>
        <Card.Header>{result.metadata.title}</Card.Header>
        <Card.Description>
          {_truncate(descriptionStripped, { length: 200 })}
        </Card.Description>
      </Card.Content>
    </Card>
  );
};

RDMRecordResultsGridItem.propTypes = {
  result: PropTypes.object.isRequired,
  index: PropTypes.string.isRequired,
};

export const RDMEmptyResults = (props) => {
  const { queryString } = props;
  return queryString === "" ? (
    <Segment.Group>
      <Segment placeholder textAlign="center" padded="very">
        <Header as="h1" align="center">
          <Header.Content>
            {i18next.t("Get started!")}
            <Header.Subheader>{i18next.t("Make your first upload!")}</Header.Subheader>
          </Header.Content>
        </Header>
        <Divider hidden />
        <Button
          positive
          icon="upload"
          floated="right"
          href={document.getElementById("invenio-search-config").dataset.depositUrl}
          content={i18next.t("New upload")}
        />
      </Segment>
    </Segment.Group>
  ) : (
    <Segment padded="very">
      <RDMNoSearchResults {...props} searchPath="/me/uploads" />
    </Segment>
  );
};

RDMEmptyResults.propTypes = {
  queryString: PropTypes.string.isRequired,
};

const appName = "InvenioAppRdm.DashboardUploads";

export const DashboardUploadsSearchLayout = DashboardSearchLayoutHOC({
  searchBarPlaceholder: i18next.t("Search in my uploads..."),
  newBtn: (
    <Button
      positive
      icon="upload"
      href={document.getElementById("invenio-search-config").dataset.depositUrl}
      content={i18next.t("New upload")}
      floated="right"
    />
  ),
  appName: appName,
  mineLabel: i18next.t("My uploads"),
  showSharedFilters: true,
});

const ContribSearchAppFacetsWithConfig = parametrize(ContribSearchAppFacets, {
  toggle: true,
});

const DashboardResultViewWAppName = parametrize(DashboardResultView, {
  appName: appName,
});

export const defaultComponents = {
  [`${appName}.BucketAggregation.element`]: ContribBucketAggregationElement,
  [`${appName}.BucketAggregationValues.element`]: ContribBucketAggregationValuesElement,
  [`${appName}.RangeFacet.element`]: ContribRangeFacetElement,
  [`${appName}.Count.element`]: RDMCountComponent,
  [`${appName}.EmptyResults.element`]: RDMEmptyResults,
  [`${appName}.ResultsList.item`]: RDMRecordResultsListItem,
  [`${appName}.ResultsGrid.item`]: RDMRecordResultsGridItem,
  [`${appName}.SearchApp.facets`]: ContribSearchAppFacetsWithConfig,
  [`${appName}.SearchApp.layout`]: DashboardUploadsSearchLayout,
  [`${appName}.SearchApp.results`]: DashboardResultViewWAppName,
  [`${appName}.SearchBar.element`]: RDMRecordSearchBarElement,
  [`${appName}.SearchFilters.Toggle.element`]: RDMToggleComponent,
};
const overriddenComponents = overrideStore.getAll();

createSearchAppInit(
  { ...defaultComponents, ...overriddenComponents },
  true,
  "invenio-search-config",
  true
);
