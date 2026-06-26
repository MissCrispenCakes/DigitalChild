/* GRIMdata — Source Transparency Watch
 *
 * Renders the peer-source transparency timeline from the static dataset at
 * /transparency-watch/data/transparency.json (built by
 * utils/build_transparency_watch_data.py). Pure static DOM; no server/Plotly.
 * Works with Material for MkDocs "navigation.instant" via document$.
 */
(function () {
  "use strict";

  var TYPE_LABEL = {
    dataset: "Dataset",
    document: "Document/legal files",
    api: "API / endpoint",
    structure: "Open-data / structure"
  };

  var _data = null;

  function el(id) { return document.getElementById(id); }

  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function dataUrl() {
    var p = window.location.pathname;
    var seg = "/transparency-watch/";
    var i = p.indexOf(seg);
    var base = i >= 0 ? p.slice(0, i + seg.length) : seg;
    return base + "data/transparency.json";
  }

  function badge(type) {
    return '<span class="tw-badge tw-badge-' + esc(type) + '">' +
      esc(TYPE_LABEL[type] || type) + "</span>";
  }

  function link(url) {
    if (!url) return "";
    return ' <a class="tw-link" href="' + esc(url) + '" target="_blank" rel="noopener noreferrer">↗</a>';
  }

  function getState() {
    var t = el("tw-f-type");
    var top = el("tw-f-topical");
    return { type: t ? t.value : "all", topicalOnly: top ? top.checked : false };
  }

  function passes(ev, st) {
    if (st.type !== "all" && ev.type !== st.type) return false;
    if (st.topicalOnly && !ev.topical) return false;
    return true;
  }

  function renderTimeline() {
    var host = el("tw-timeline");
    if (!host || !_data) return;
    var st = getState();
    var events = _data.timeline.filter(function (e) { return passes(e, st); });
    if (!events.length) {
      host.innerHTML = '<p class="sc-hint">No signals match the current filter.</p>';
      return;
    }
    var html = events.map(function (e) {
      return '<div class="tw-event tw-' + esc(e.type) + '">' +
        '<span class="tw-date">' + esc(e.date) + "</span>" +
        badge(e.type) +
        '<span class="tw-src">' + esc(e.source) + "</span>" +
        '<span class="tw-evlabel">' + esc(e.label) +
        (e.topical ? ' <span class="tw-star" title="On-topic for this source">★</span>' : "") +
        "</span>" + link(e.url) + "</div>";
    }).join("");
    host.innerHTML = html;
    var c = el("tw-count");
    if (c) c.textContent = events.length + " of " + _data.timeline.length + " signals";
  }

  function renderSources() {
    var host = el("tw-sources");
    if (!host || !_data) return;
    var st = getState();
    var html = _data.sources.map(function (s) {
      var sigs = s.signals.filter(function (sig) {
        if (st.type !== "all" && sig.type !== st.type) return false;
        if (st.topicalOnly && !sig.topical) return false;
        return true;
      });
      var empty = (s.query_ok === false)
        ? '<li class="sc-hint">Archive query incomplete — not yet assessed.</li>'
        : '<li class="sc-hint">No transparency signals detected yet.</li>';
      var rows = sigs.length ? sigs.map(function (sig) {
        return "<li>" + badge(sig.type) +
          '<span class="tw-evlabel">' + esc(sig.label) + "</span>" +
          '<span class="tw-seen">since <strong>' + esc(sig.display_date) + "</strong>" +
          (sig.count > 1 ? ' · ' + sig.count + " captures" : "") + "</span>" +
          (sig.topical ? ' <span class="tw-star" title="On-topic">★</span>' : "") +
          link(sig.display_url) + "</li>";
      }).join("") : empty;
      var span = (s.first_signal || "?") + " – " + (s.last_signal || "?");
      return '<div class="tw-card">' +
        '<div class="tw-card-head"><h3 class="no-rainbow">' + esc(s.name) + "</h3>" +
        '<a class="tw-link" href="' + esc(s.homepage) + '" target="_blank" rel="noopener noreferrer">site ↗</a></div>' +
        '<p class="tw-span">signals observed ' + esc(span) + "</p>" +
        '<ul class="tw-siglist">' + rows + "</ul></div>";
    }).join("");
    host.innerHTML = html;
  }

  function renderAll() { renderTimeline(); renderSources(); }

  function init() {
    if (!el("tw-app")) return;  // not the transparency page
    var loading = el("tw-loading");
    fetch(dataUrl())
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (data) {
        _data = data;
        var meta = el("tw-meta");
        if (meta) {
          meta.textContent = data.meta.source_count + " sources · " +
            data.timeline.length + " signals · generated " +
            (data.meta.generated_at || "").slice(0, 10);
        }
        ["tw-f-type", "tw-f-topical"].forEach(function (id) {
          var n = el(id);
          if (n && !n.dataset.ready) { n.addEventListener("change", renderAll); n.dataset.ready = "1"; }
        });
        renderAll();
        if (loading) loading.style.display = "none";
      })
      .catch(function (err) {
        console.error("Transparency watch error:", err);
        if (loading) loading.innerHTML = "<strong>Could not load the transparency dataset.</strong>";
      });
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
