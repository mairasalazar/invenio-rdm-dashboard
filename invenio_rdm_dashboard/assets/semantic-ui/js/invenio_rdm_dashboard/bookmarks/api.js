/*
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: MIT
 */

const BASE_URL = "/api/me/bookmarks";

// function from https://www.w3schools.com/js/js_cookies.asp
function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

async function request(url, { headers, ...options } = {}) {
  const response = await fetch(url, {
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
      ...headers,
    },
    ...options,
  });
  if (!response.ok && response.status !== 404) {
    throw new Error(`Bookmarks API error: ${response.status} on ${url}`);
  }
  return response;
}

export const bookmarksApi = {
  async isBookmarked(resourceType, resourcePid) {
    const response = await request(`${BASE_URL}/${resourceType}/${resourcePid}`);
    return response.status === 200;
  },

  async create(resourceType, resourcePid) {
    return request(BASE_URL, {
      method: "POST",
      body: JSON.stringify({ resource_type: resourceType, resource_pid: resourcePid }),
    });
  },

  async remove(resourceType, resourcePid) {
    return request(`${BASE_URL}/${resourceType}/${resourcePid}`, {
      method: "DELETE",
    });
  },

  async list({ resourceType, sort = "bookmarked-desc", page = 1, size = 25 } = {}) {
    const params = new URLSearchParams({ sort, page, size });
    if (resourceType) params.set("resource_type", resourceType);
    const response = await request(`${BASE_URL}?${params.toString()}`);
    return response.json();
  },
};
