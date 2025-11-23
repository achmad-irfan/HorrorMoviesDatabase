document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("movieSearchInput");
  const dropdown = document.getElementById("searchResults");

  if (!input || !dropdown) {
    console.error("Search elements not found in DOM.");
    return;
  }

  let controller = null;
  let highlightedIndex = -1;

  function escapeHtml(s) {
    return s.replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        }[c])
    );
  }

  function debounce(fn, ms = 300) {
    let t;
    return function (...args) {
      clearTimeout(t);
      t = setTimeout(() => fn.apply(this, args), ms);
    };
  }

  async function fetchResults(q) {
    if (controller) controller.abort();
    controller = new AbortController();

    try {
      const res = await fetch(`/search_api/?q=${encodeURIComponent(q)}`, {
        signal: controller.signal,
      });

      if (!res.ok) return [];

      const json = await res.json();
      return json.results || [];
    } catch (e) {
      if (e.name === "AbortError") return null;
      console.error("Search API error:", e);
      return [];
    }
  }

  function render(results) {
    dropdown.innerHTML = "";
    highlightedIndex = -1;

    if (!results || results.length === 0) {
      dropdown.hidden = true;
      return;
    }

    results.forEach((r) => {
      const item = document.createElement("div");
      item.setAttribute("role", "option");
      item.className = "search-item";
      item.tabIndex = -1;
      item.dataset.id = r.id;

      item.textContent = `${r.title} ${r.year ? "(" + r.year + ")" : ""}`;

      item.addEventListener("click", () => {
        window.location.href = `/movie/${r.id}/`;
      });

      dropdown.appendChild(item);
    });

    dropdown.hidden = false;
  }

  const handleInput = debounce(async function (e) {
    const q = e.target.value.trim();

    if (q.length < 2) {
      dropdown.hidden = true;
      return;
    }

    const results = await fetchResults(q);
    if (results === null) return;

    render(results);
  }, 300);

  input.addEventListener("input", handleInput);

  document.addEventListener("click", (ev) => {
    if (!ev.target.closest(".nav-search")) dropdown.hidden = true;
  });

  input.addEventListener("keydown", (e) => {
    const items = dropdown.querySelectorAll(".search-item");

    if (dropdown.hidden || items.length === 0) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      highlightedIndex = Math.min(highlightedIndex + 1, items.length - 1);
      items[highlightedIndex].focus();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      highlightedIndex = Math.max(highlightedIndex - 1, 0);
      items[highlightedIndex].focus();
    } else if (e.key === "Enter") {
      const focused = document.activeElement;
      if (focused && focused.classList.contains("search-item")) {
        focused.click();
      }
    } else if (e.key === "Escape") {
      dropdown.hidden = true;
      input.blur();
    }
  });
});
