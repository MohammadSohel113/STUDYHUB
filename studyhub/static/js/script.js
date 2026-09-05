document.addEventListener("DOMContentLoaded", function () {
  // ---- Theme toggle ----
  var root = document.documentElement;
  var toggle = document.getElementById("themeToggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var current = root.getAttribute("data-theme") === "light" ? "dark" : "light";
      root.setAttribute("data-theme", current);
      localStorage.setItem("studyhub-theme", current);
    });
  }

  // ---- Mobile nav ----
  var hamburger = document.getElementById("hamburger");
  var nav = document.getElementById("mainNav");
  if (hamburger && nav) {
    hamburger.addEventListener("click", function () {
      var isOpen = nav.classList.toggle("open");
      hamburger.setAttribute("aria-expanded", isOpen);
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { nav.classList.remove("open"); });
    });
  }

  // ---- Copy code buttons ----
  document.querySelectorAll(".copy-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var target = document.getElementById(btn.dataset.target);
      if (!target) return;
      navigator.clipboard.writeText(target.innerText).then(function () {
        var original = btn.innerHTML;
        btn.innerHTML = "✓ Copied";
        btn.classList.add("copied");
        setTimeout(function () {
          btn.innerHTML = original;
          btn.classList.remove("copied");
        }, 1600);
      });
    });
  });

  // ---- Quiz: require an answer before enabling submit (soft nudge, not blocking) ----
  var quizForm = document.getElementById("quizForm");
  if (quizForm) {
    quizForm.addEventListener("submit", function (e) {
      var groups = quizForm.querySelectorAll("[data-question-group]");
      var unanswered = 0;
      groups.forEach(function (g) {
        if (!g.querySelector("input:checked")) unanswered++;
      });
      if (unanswered > 0) {
        var proceed = confirm(unanswered + " question(s) left unanswered. Submit anyway?");
        if (!proceed) e.preventDefault();
      }
    });
  }
});
