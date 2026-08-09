(() => {
  const buttons = Array.from(document.querySelectorAll(".work-cat"));
  const panels = Array.from(document.querySelectorAll("[data-panel]"));
  if (!buttons.length || !panels.length) return;

  const activate = (id, { updateHash = true } = {}) => {
    buttons.forEach((btn) => {
      const on = btn.dataset.cat === id;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-selected", on ? "true" : "false");
      if (on) {
        btn.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
      }
    });

    panels.forEach((panel) => {
      const on = panel.dataset.panel === id;
      panel.classList.toggle("is-hidden", !on);
      if (on) panel.removeAttribute("hidden");
      else panel.setAttribute("hidden", "");
    });

    if (updateHash && window.location.hash.replace("#", "") !== id) {
      history.replaceState(null, "", `#${id}`);
    }
  };

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => activate(btn.dataset.cat));
  });

  window.addEventListener("hashchange", () => {
    const hash = window.location.hash.replace("#", "");
    if (hash && buttons.some((b) => b.dataset.cat === hash)) {
      activate(hash, { updateHash: false });
    }
  });

  const hash = window.location.hash.replace("#", "");
  if (hash && buttons.some((b) => b.dataset.cat === hash)) {
    activate(hash, { updateHash: false });
  }
})();
