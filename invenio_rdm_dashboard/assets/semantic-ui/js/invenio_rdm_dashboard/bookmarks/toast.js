/*
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: MIT
 *
 * A minimal, dependency-free toast. BookmarkStar is mounted as many
 * independent React roots across different pages/bundles (list items,
 * landing pages, favourites), so a shared React context for this would
 * mean threading a provider through every one of them; a single
 * document-level DOM node that any of them can push a message into is
 * simpler and avoids stacking a toast per star.
 */

function getContainer() {
  let container = document.getElementById("invenio-rdm-dashboard-toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "invenio-rdm-dashboard-toast-container";
    container.style.position = "fixed";
    container.style.bottom = "20px";
    container.style.right = "20px";
    container.style.zIndex = 9999;
    container.style.display = "flex";
    container.style.flexDirection = "column";
    container.style.gap = "0.5rem";
    document.body.appendChild(container);
  }
  return container;
}

export function showToast(message, { type = "positive", duration = 2500 } = {}) {
  const container = getContainer();

  const toast = document.createElement("div");
  toast.className = `ui ${type} message`;
  toast.style.boxShadow = "0 2px 8px rgba(0, 0, 0, 0.2)";
  toast.style.opacity = "0";
  toast.style.transition = "opacity 0.2s ease";
  toast.textContent = message;

  container.appendChild(toast);
  // Next frame, so the opacity transition actually runs.
  requestAnimationFrame(() => {
    toast.style.opacity = "1";
  });

  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 200);
  }, duration);
}
