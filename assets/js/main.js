(() => {
  const year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  const toggle = document.querySelector(".menu-toggle");
  const nav = document.getElementById("site-nav");
  if (toggle && nav) {
    const setOpen = (open) => {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    };

    toggle.addEventListener("click", () => {
      setOpen(!nav.classList.contains("is-open"));
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => setOpen(false));
    });
  }

  const form = document.getElementById("enquiry-form");
  if (!form) return;

  const snackbar = document.getElementById("snackbar");
  const submitBtn = form.querySelector('button[type="submit"]');
  let snackTimer;

  const showSnackbar = (message, tone) => {
    if (!snackbar) return;
    snackbar.textContent = message;
    snackbar.classList.toggle("snackbar-error", tone === "error");
    snackbar.hidden = false;
    snackbar.classList.add("is-visible");
    window.clearTimeout(snackTimer);
    snackTimer = window.setTimeout(() => {
      snackbar.classList.remove("is-visible");
      snackTimer = window.setTimeout(() => {
        snackbar.hidden = true;
      }, 250);
    }, 4200);
  };

  const interestField = form.elements.namedItem("interest");
  const params = new URLSearchParams(window.location.search);
  const requested = params.get("interest");
  if (requested && interestField) {
    const allowed = Array.from(interestField.options).map((opt) => opt.value);
    if (allowed.includes(requested)) interestField.value = requested;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const subjectField = form.elements.namedItem("_subject");
    const interest = interestField ? String(interestField.value) : "other";
    const name = String(form.elements.namedItem("name")?.value || "").trim();
    if (subjectField) subjectField.value = `Enquiry: ${interest} — ${name || "Website enquiry"}`;

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = "Sending…";
    }

    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" },
      });

      if (!response.ok) throw new Error("Formspree rejected the submission");

      form.reset();
      if (requested && interestField && Array.from(interestField.options).some((opt) => opt.value === requested)) {
        interestField.value = requested;
      }
      showSnackbar("Message sent. I’ll get back to you by email.");
    } catch {
      showSnackbar("The message could not be sent. Please email me directly.", "error");
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = "Send Message";
      }
    }
  });
})();
