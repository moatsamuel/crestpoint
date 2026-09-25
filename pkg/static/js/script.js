/* ==========================================================================
   CrestPoint Clinic — Global Script (frontend only)
   - Mobile navigation menu
   - Password show/hide toggles
   - Demo-only form handling (nothing is sent anywhere)
   - Footer year + active nav link
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {

  /* ------------------------------------------------------------------
     1. Mobile navigation (hamburger menu)
     ------------------------------------------------------------------ */
  const navToggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (navToggle && navLinks) {
    navToggle.addEventListener("click", function () {
      const isOpen = navLinks.classList.toggle("open");
      navToggle.classList.toggle("open", isOpen);
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    // Close the menu when a link inside it is clicked
    navLinks.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navLinks.classList.remove("open");
        navToggle.classList.remove("open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ------------------------------------------------------------------
     2. Password show / hide buttons
        Usage: <button class="toggle-pass" data-toggle="#password">👁</button>
     ------------------------------------------------------------------ */
  document.querySelectorAll(".toggle-pass").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const input = document.querySelector(btn.getAttribute("data-toggle"));
      if (!input) return;
      const show = input.type === "password";
      input.type = show ? "text" : "password";
      btn.textContent = show ? "🙈" : "👁";
      btn.setAttribute("aria-label", show ? "Hide password" : "Show password");
    });
  });

  /* ------------------------------------------------------------------
     3. Demo-only form handling
        IMPORTANT: No data leaves this page. We simply stop the browser
        from submitting and show a friendly demo message instead.
     ------------------------------------------------------------------ */
  document.querySelectorAll("form[data-demo]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault(); // frontend only — no submission anywhere

      const status = form.querySelector(".form-status");
      if (status) {
        status.textContent = form.getAttribute("data-demo-message") ||
          "This is a frontend demo — form submission is not connected to any backend.";
        status.classList.add("show");

        // Hide the message again after a few seconds
        setTimeout(function () {
          status.classList.remove("show");
        }, 6000);
      }
    });
  });

  /* ------------------------------------------------------------------
     4. Footer year (e.g. "© 2026 CrestPoint Clinic")
     ------------------------------------------------------------------ */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ------------------------------------------------------------------
     5. Highlight the current page in the navigation
        (Compares the data-page value on each link with <body data-page>)
     ------------------------------------------------------------------ */
  const bodyPage = document.body.getAttribute("data-page");
  if (bodyPage) {
    document.querySelectorAll(".nav-links a[data-page]").forEach(function (link) {
      if (link.getAttribute("data-page") === bodyPage) {
        link.classList.add("active");
      }
    });
  }
});
