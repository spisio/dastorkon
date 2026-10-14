// Region filter on the home page, serving scaler on recipe pages.
(function () {
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }

  var filters = document.querySelector(".filters");
  if (filters) {
    var cards = document.querySelectorAll(".card");
    var empty = document.getElementById("empty");
    function apply(f) {
      var shown = 0;
      filters.querySelectorAll("button").forEach(function (b) {
        b.setAttribute("aria-pressed", String(b.dataset.f === f));
      });
      cards.forEach(function (c) {
        var on = f === "all" || c.dataset.regions.split(" ").indexOf(f) !== -1;
        c.hidden = !on;
        if (on) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    }
    filters.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      store("jd-filter", b.dataset.f);
      apply(b.dataset.f);
    });
    var saved = load("jd-filter");
    if (saved && filters.querySelector('[data-f="' + saved + '"]')) apply(saved);
  }

  var scaler = document.querySelector(".scaler");
  if (scaler) {
    var base = Number(scaler.dataset.serves);
    var n = base;
    var out = scaler.querySelector(".sv-out");
    var qs = document.querySelectorAll(".ing .q[data-q]");
    function fmt(x) {
      if (x >= 10) return String(Math.round(x));
      var fr = { 0.25: "¼", 0.5: "½", 0.75: "¾" };
      var w = Math.floor(x), f = Math.round((x - w) * 4) / 4;
      if (f === 1) return String(w + 1);
      if (fr[f]) return (w ? w : "") + fr[f];
      return String(Math.round(x * 10) / 10);
    }
    function render() {
      out.textContent = n;
      qs.forEach(function (el) {
        var u = el.dataset.u;
        el.textContent = fmt(Number(el.dataset.q) * n / base) + (u ? " " + u : "");
      });
    }
    scaler.querySelector(".sv-minus").addEventListener("click", function () { if (n > 1) { n--; render(); } });
    scaler.querySelector(".sv-plus").addEventListener("click", function () { if (n < 40) { n++; render(); } });
    render();
  }
})();
