/* =====================================================================
   main.js - the small amount of JavaScript this site needs.

   Three jobs:
     1. The mobile navigation menu.
     2. A subtle border on the header once the page is scrolled.
     3. Friendly client-side validation on the contact form.

   Everything here is an enhancement. If JavaScript fails to load, the
   navigation links still work and the contact form still submits - the
   server validates every submission regardless of what the browser does.
   ===================================================================== */

(function () {
  "use strict";

  /* ------------------------------------------------------------------
     1. Mobile navigation
  ------------------------------------------------------------------ */
  function initNav() {
    const toggle = document.querySelector("[data-nav-toggle]");
    const nav = document.querySelector("[data-nav]");
    if (!toggle || !nav) return;

    const iconOpen = toggle.querySelector("[data-nav-icon-open]");
    const iconClose = toggle.querySelector("[data-nav-icon-close]");

    function setOpen(open) {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      if (iconOpen) iconOpen.hidden = open;
      if (iconClose) iconClose.hidden = !open;
    }

    toggle.addEventListener("click", function () {
      setOpen(!nav.classList.contains("is-open"));
    });

    // Tapping a link closes the menu.
    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) setOpen(false);
    });

    // Escape closes the menu and returns focus to the button, which is
    // what keyboard users expect.
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        setOpen(false);
        toggle.focus();
      }
    });

    // Reset the menu if the window grows to desktop width while open.
    window.addEventListener("resize", function () {
      if (window.innerWidth > 860) setOpen(false);
    });
  }

  /* ------------------------------------------------------------------
     2. Header shadow on scroll
  ------------------------------------------------------------------ */
  function initHeader() {
    const header = document.querySelector("[data-header]");
    if (!header) return;

    let ticking = false;

    function update() {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
      ticking = false;
    }

    // requestAnimationFrame keeps this cheap: the work happens once per
    // frame at most, rather than on every single scroll event.
    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          window.requestAnimationFrame(update);
          ticking = true;
        }
      },
      { passive: true }
    );

    update();
  }

  /* ------------------------------------------------------------------
     3. Contact form validation

     This mirrors the rules in app/forms/contact.py so mistakes are caught
     before a page reload. It is convenience only - the server enforces
     the same rules and is the one that actually protects us.
  ------------------------------------------------------------------ */
  const RULES = {
    name: { required: true, min: 2, max: 120, label: "your name" },
    email: { required: true, email: true, max: 255, label: "your email address" },
    company: { required: false, max: 160, label: "your company" },
    subject: { required: true, min: 3, max: 200, label: "a subject" },
    message: { required: true, min: 10, max: 4000, label: "your message" }
  };

  // Deliberately simple: it catches typos such as a missing "@" without
  // rejecting unusual but valid addresses. The server does the real check.
  const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function validateField(input) {
    const rule = RULES[input.name];
    if (!rule) return null;

    const value = input.value.trim();

    if (!value) {
      return rule.required ? "Please enter " + rule.label + "." : null;
    }
    if (rule.min && value.length < rule.min) {
      return "Please use at least " + rule.min + " characters.";
    }
    if (rule.max && value.length > rule.max) {
      return "Please use no more than " + rule.max + " characters.";
    }
    if (rule.email && !EMAIL_PATTERN.test(value)) {
      return "That does not look like a valid email address.";
    }
    return null;
  }

  function showError(input, message) {
    const field = input.closest(".form-field");
    if (!field) return;

    let error = field.querySelector(".form-error");

    if (!message) {
      field.classList.remove("has-error");
      input.classList.remove("is-invalid");
      input.setAttribute("aria-invalid", "false");
      if (error) error.remove();
      return;
    }

    field.classList.add("has-error");
    input.classList.add("is-invalid");
    input.setAttribute("aria-invalid", "true");

    if (!error) {
      error = document.createElement("p");
      error.className = "form-error";
      error.setAttribute("role", "alert");
      error.id = input.id + "-error";
      field.appendChild(error);
    }
    error.textContent = message;
    input.setAttribute("aria-describedby", error.id);
  }

  function initForm() {
    const form = document.querySelector("[data-validate]");
    if (!form) return;

    const inputs = Array.prototype.slice
      .call(form.querySelectorAll("input, textarea"))
      .filter(function (input) {
        return RULES[input.name];
      });

    inputs.forEach(function (input) {
      // Check when the visitor leaves a field ...
      input.addEventListener("blur", function () {
        showError(input, validateField(input));
      });
      // ... and clear the error as soon as they start fixing it.
      input.addEventListener("input", function () {
        if (input.classList.contains("is-invalid")) {
          showError(input, validateField(input));
        }
      });
    });

    form.addEventListener("submit", function (event) {
      let firstInvalid = null;

      inputs.forEach(function (input) {
        const message = validateField(input);
        showError(input, message);
        if (message && !firstInvalid) firstInvalid = input;
      });

      if (firstInvalid) {
        event.preventDefault();
        firstInvalid.focus();
        firstInvalid.scrollIntoView({ block: "center", behavior: "smooth" });
        return;
      }

      // Stops an impatient double-click from sending two messages.
      const submit = form.querySelector('[type="submit"]');
      if (submit) {
        submit.disabled = true;
        submit.value = "Sending...";
      }
    });
  }

  /* ------------------------------------------------------------------
     Start everything
  ------------------------------------------------------------------ */
  function init() {
    initNav();
    initHeader();
    initForm();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
