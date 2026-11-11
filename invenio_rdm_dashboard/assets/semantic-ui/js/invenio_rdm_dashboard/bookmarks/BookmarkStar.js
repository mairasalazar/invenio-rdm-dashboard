/*
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: MIT
 */

import React, { useEffect, useState } from "react";
import { Icon } from "semantic-ui-react";
import { bookmarksApi } from "./api";
import { showToast } from "./toast";

/**
 * Star toggle passed as the `titleActions` prop to RecordsResultsListItem,
 * CommunityItem, and used directly on the record/community landing pages.
 *
 * `result` is whatever the call site has on hand - a search hit or
 * `{ id: pid }` - only `result.id` is read; `resourceType` must match a
 * key in BOOKMARKS_RESOURCE_TYPES on the backend ("record" or
 * "community").
 */
export const BookmarkStar = ({ result, resourceType = "record" }) => {
  const resourcePid = result?.id;
  const [bookmarked, setBookmarked] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let active = true;
    if (resourcePid) {
      bookmarksApi
        .isBookmarked(resourceType, resourcePid)
        .then((value) => {
          if (active) setBookmarked(value);
        })
        .catch((err) => {
          console.error("Failed to check bookmark status", err);
        });
    }
    return () => {
      active = false;
    };
  }, [resourceType, resourcePid]);

  const toggle = async (event) => {
    event.preventDefault();
    if (loading || !resourcePid) return;
    setLoading(true);
    try {
      if (bookmarked) {
        await bookmarksApi.remove(resourceType, resourcePid);
        setBookmarked(false);
        showToast("Removed from favourites");
      } else {
        await bookmarksApi.create(resourceType, resourcePid);
        setBookmarked(true);
        showToast("Added to favourites");
      }
    } catch (err) {
      console.error("Failed to toggle bookmark", err);
      showToast("Something went wrong, please try again", { type: "negative" });
    } finally {
      setLoading(false);
    }
  };

  if (!resourcePid) return null;

  return (
    <Icon
      name={bookmarked ? "star" : "star outline"}
      color={bookmarked ? "yellow" : undefined}
      link
      disabled={loading}
      onClick={toggle}
      aria-label={bookmarked ? "Remove bookmark" : "Add bookmark"}
      title={bookmarked ? "Remove bookmark" : "Add bookmark"}
      // Semantic's `.ui.header > .icon` rule sizes icons at 1.5em of the
      // *header's* font-size, and that font-size varies a lot across the
      // different host headers this is dropped into ("ui medium header"
      // vs. an Item.Header, etc.) - fixing the size in absolute units
      // here makes it look the same everywhere, regardless of context.
      // `textDecoration: none` guards against being nested inside an
      // anchor whose hover state would otherwise underline it.
      style={{ fontSize: "1rem", textDecoration: "none" }}
    />
  );
};
