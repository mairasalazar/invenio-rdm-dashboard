/*
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: MIT
 */

import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom";
import {
  Card,
  Checkbox,
  Container,
  Dropdown,
  Grid,
  Item,
  List,
  Loader,
  Message,
} from "semantic-ui-react";
import RecordsResultsListItem from "@js/invenio_app_rdm/components/RecordsResultsListItem";
import { CommunityItem } from "@js/invenio_communities/community";
import { bookmarksApi } from "./bookmarks/api";
import { BookmarkStar } from "./bookmarks/BookmarkStar";
import { CommunityBookmarkStar } from "./bookmarks/communityOverrides";

const API_PATHS = {
  record: (pid) => `/api/records/${pid}`,
  community: (pid) => `/api/communities/${pid}`,
};

const RESOURCE_TYPE_OPTIONS = [
  { value: "", label: "All" },
  { value: "record", label: "Records" },
  { value: "community", label: "Communities" },
];

const SORT_OPTIONS = [
  { key: "bookmarked-desc", value: "bookmarked-desc", text: "Recently bookmarked" },
  { key: "bookmarked-asc", value: "bookmarked-asc", text: "Oldest bookmarked" },
  { key: "title-asc", value: "title-asc", text: "Title (A-Z)" },
  { key: "title-desc", value: "title-desc", text: "Title (Z-A)" },
];

// Fetching each bookmark's full resource again (rather than relying on
// the already-resolved metadata the bookmarks list endpoint returns)
// gets us the same UI-JSON shape (`ui.*`, `stats.*`, ...) that
// RecordsResultsListItem / CommunityItem expect, so a favourite renders
// identically to how it does in its own search results list.
async function fetchResult(resourceType, resourcePid) {
  const response = await fetch(API_PATHS[resourceType](resourcePid), {
    credentials: "same-origin",
    headers: { Accept: "application/vnd.inveniordm.v1+json" },
  });
  if (!response.ok) return null;
  return response.json();
}

const FavouriteItem = ({ resourceType, resourcePid, result }) => {
  if (resourceType === "community") {
    return (
      <CommunityItem
        result={result}
        titleActions={CommunityBookmarkStar}
        showEditButton={false}
      />
    );
  }
  return <RecordsResultsListItem result={result} titleActions={BookmarkStar} />;
};

const FavouritesPage = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [items, setItems] = useState([]);
  const [resourceType, setResourceType] = useState("");
  const [sort, setSort] = useState("bookmarked-desc");

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError(null);

    bookmarksApi
      .list({ resourceType: resourceType || undefined, sort })
      .then(async ({ hits }) => {
        const resolved = await Promise.all(
          hits.hits.map(async ({ resource_type, resource_pid }) => {
            const result = await fetchResult(resource_type, resource_pid);
            return result && { resourceType: resource_type, resourcePid: resource_pid, result };
          })
        );
        if (active) setItems(resolved.filter(Boolean));
      })
      .catch((err) => {
        console.error("Failed to load favourites", err);
        if (active) setError(err);
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [resourceType, sort]);

  return (
    <Container>
      <Grid>
        <Grid.Row>
          <Grid.Column mobile={16} tablet={16} computer={4}>
            <Card className="borderless facet">
              <Card.Content>
                <Card.Header as="h2">Resource type</Card.Header>
                <List link>
                  {RESOURCE_TYPE_OPTIONS.map((option) => (
                    <List.Item key={option.value} className="facet-wrapper">
                      <Checkbox
                        radio
                        label={option.label}
                        checked={resourceType === option.value}
                        onChange={() => setResourceType(option.value)}
                      />
                    </List.Item>
                  ))}
                </List>
              </Card.Content>
            </Card>
          </Grid.Column>

          <Grid.Column mobile={16} tablet={16} computer={12}>
            <div className="flex justify-space-between align-items-center mb-10">
              <div />
              <div>
                <label className="mr-10">Sort by</label>
                <Dropdown
                  selection
                  options={SORT_OPTIONS}
                  value={sort}
                  onChange={(_, { value }) => setSort(value)}
                />
              </div>
            </div>

            {loading && <Loader active inline="centered" />}

            {!loading && error && (
              <Message negative>
                <Message.Header>Could not load your favourites</Message.Header>
                <p>
                  Please try reloading the page. If this keeps happening, contact
                  support.
                </p>
              </Message>
            )}

            {!loading && !error && items.length === 0 && (
              <p>
                {resourceType
                  ? "No favourites match this filter."
                  : "You haven't bookmarked anything yet."}
              </p>
            )}

            {!loading && !error && items.length > 0 && (
              <Item.Group divided relaxed link>
                {items.map(({ resourceType: itemType, resourcePid, result }) => (
                  <FavouriteItem
                    key={`${itemType}-${resourcePid}`}
                    resourceType={itemType}
                    resourcePid={resourcePid}
                    result={result}
                  />
                ))}
              </Item.Group>
            )}
          </Grid.Column>
        </Grid.Row>
      </Grid>
    </Container>
  );
};

const root = document.getElementById("invenio-rdm-dashboard-favourites");
if (root) {
  ReactDOM.render(<FavouritesPage />, root);
}
