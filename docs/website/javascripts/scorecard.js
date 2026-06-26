/* GRIMdata — Scorecard visualizations & data explorer
 *
 * Renders the Digital Rights Scorecard from the static dataset published at
 * /scorecard/data/scorecard.json (built by utils/build_scorecard_viz_data.py).
 *
 * Pure static: no API/server required. Plotly is loaded from CDN on demand,
 * only when a scorecard container is present on the page. Designed to work
 * with Material for MkDocs "navigation.instant" via the document$ observable.
 */
(function () {
  "use strict";

  var PLOTLY_SRC = "https://cdn.plot.ly/plotly-2.27.0.min.js";

  // Score → colour (0 worst → 2 best). Used for table heatmap cells & bars.
  var SCORE_COLORS = { 0: "#d64545", 1: "#e8a33d", 2: "#2e8b57" };
  var SCORE_LABELS = { 0: "0 — Worst", 1: "1 — Partial", 2: "2 — Best" };

  var _dataPromise = null;
  var _plotlyPromise = null;

  /* ---------- loaders (memoized) ---------- */

  function dataUrl() {
    // Build a path to /scorecard/data/scorecard.json that survives custom
    // domains (root) and project subpaths alike.
    var p = window.location.pathname;
    var idx = p.indexOf("/scorecard/");
    var base = idx >= 0 ? p.slice(0, idx + "/scorecard/".length) : "/scorecard/";
    return base + "data/scorecard.json";
  }

  function loadData() {
    if (!_dataPromise) {
      _dataPromise = fetch(dataUrl())
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status + " for " + dataUrl());
          return r.json();
        });
    }
    return _dataPromise;
  }

  function loadPlotly() {
    if (typeof window.Plotly !== "undefined") return Promise.resolve(window.Plotly);
    if (!_plotlyPromise) {
      _plotlyPromise = new Promise(function (resolve, reject) {
        var s = document.createElement("script");
        s.src = PLOTLY_SRC;
        s.onload = function () { resolve(window.Plotly); };
        s.onerror = function () { reject(new Error("Failed to load Plotly")); };
        document.head.appendChild(s);
      });
    }
    return _plotlyPromise;
  }

  /* ---------- helpers ---------- */

  function el(id) { return document.getElementById(id); }

  function plotlyLayout(extra) {
    var base = {
      margin: { t: 40, r: 10, b: 40, l: 10 },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: { color: getComputedStyle(document.body).getPropertyValue("--md-default-fg-color") || "#333" },
      autosize: true
    };
    return Object.assign(base, extra || {});
  }

  var PLOT_CFG = { responsive: true, displaylogo: false,
    modeBarButtonsToRemove: ["lasso2d", "select2d", "autoScale2d"] };

  /* ---------- charts ---------- */

  var GREEN_TO_RED = [[0, "#d64545"], [0.5, "#e8a33d"], [1, "#2e8b57"]];
  var RED_TO_GREEN = [[0, "#2e8b57"], [0.5, "#e8a33d"], [1, "#d64545"]];
  var MAP_METRICS = {
    protection_score: { title: "Protection Score", range: [0, 20], reverse: false },
    risk_index: { title: "Risk Index", range: [0, 100], reverse: true },
    documented: { title: "Documented (0–10)", range: [0, 10], reverse: false }
  };

  function renderMap(Plotly, data) {
    var node = el("sc-map");
    if (!node) return;
    var metricSel = el("sc-map-metric");
    var metric = metricSel ? metricSel.value : "protection_score";
    var cfg = MAP_METRICS[metric] || MAP_METRICS.protection_score;

    var rows = data.countries.filter(function (c) {
      return c.iso3 && c[metric] !== null && c[metric] !== undefined;
    });

    var trace = {
      type: "choropleth",
      locationmode: "ISO-3",
      locations: rows.map(function (c) { return c.iso3; }),
      z: rows.map(function (c) { return c[metric]; }),
      customdata: rows.map(function (c) { return c.country; }),
      text: rows.map(function (c) {
        return "<b>" + c.country + "</b><br>" +
          (c.region || "—") + "<br>" +
          "Protection: " + fmt(c.protection_score) + "/20<br>" +
          "Risk: " + fmt(c.risk_index) + "/100<br>" +
          "Documented: " + fmt(c.documented) + "/10<br>" +
          "<i>click for details</i>";
      }),
      hoverinfo: "text",
      colorscale: cfg.reverse ? RED_TO_GREEN : GREEN_TO_RED,
      zmin: cfg.range[0],
      zmax: cfg.range[1],
      colorbar: { title: cfg.title, thickness: 12 },
      marker: { line: { color: "rgba(120,120,120,0.4)", width: 0.4 } }
    };

    Plotly.newPlot(node, [trace], plotlyLayout({
      title: "Digital Rights — " + cfg.title + " by Country",
      geo: { showframe: false, showcoastlines: false, projection: { type: "natural earth" }, bgcolor: "rgba(0,0,0,0)" },
      margin: { t: 40, r: 0, b: 0, l: 0 }, height: 460
    }), PLOT_CFG);

    // Click a country to open its detail panel (when a host exists on the page).
    node.on("plotly_click", function (ev) {
      if (ev && ev.points && ev.points.length) {
        var name = ev.points[0].customdata;
        if (name) showDetail(data, name);
      }
    });
  }

  function renderIndicators(Plotly, data) {
    var node = el("sc-indicators");
    if (!node) return;
    var inds = data.meta.indicators;
    // counts[score] = array aligned with inds
    var counts = { 0: [], 1: [], 2: [] };
    inds.forEach(function (ind) {
      var tally = { 0: 0, 1: 0, 2: 0 };
      data.countries.forEach(function (c) {
        var v = c.scores[ind.key];
        if (v === 0 || v === 1 || v === 2) tally[v] += 1;
      });
      counts[0].push(tally[0]); counts[1].push(tally[1]); counts[2].push(tally[2]);
    });
    var labels = inds.map(function (i) { return i.label; });
    var traces = [2, 1, 0].map(function (s) {
      return {
        type: "bar", orientation: "h", name: SCORE_LABELS[s],
        y: labels, x: counts[s], marker: { color: SCORE_COLORS[s] },
        hovertemplate: "%{y}<br>" + SCORE_LABELS[s] + ": %{x} countries<extra></extra>"
      };
    });
    Plotly.newPlot(node, traces, plotlyLayout({
      title: "How countries score on each indicator",
      barmode: "stack", height: 420,
      xaxis: { title: "Number of countries" },
      yaxis: { automargin: true },
      legend: { orientation: "h", y: -0.15 }
    }), PLOT_CFG);
  }

  function renderRegions(Plotly, data) {
    var node = el("sc-regions");
    if (!node) return;
    var sums = {}, n = {};
    data.countries.forEach(function (c) {
      if (!c.region || c.protection_score === null) return;
      sums[c.region] = (sums[c.region] || 0) + c.protection_score;
      n[c.region] = (n[c.region] || 0) + 1;
    });
    var regions = Object.keys(sums).map(function (r) {
      return { region: r, avg: sums[r] / n[r], n: n[r] };
    }).sort(function (a, b) { return b.avg - a.avg; });

    Plotly.newPlot(node, [{
      type: "bar",
      x: regions.map(function (r) { return r.region; }),
      y: regions.map(function (r) { return Math.round(r.avg * 10) / 10; }),
      marker: { color: regions.map(function (r) {
        var t = r.avg / 20; return t < 0.4 ? "#d64545" : t < 0.65 ? "#e8a33d" : "#2e8b57"; }) },
      text: regions.map(function (r) { return (Math.round(r.avg * 10) / 10) + " (n=" + r.n + ")"; }),
      textposition: "outside",
      hovertemplate: "%{x}<br>Avg protection: %{y}/20<extra></extra>"
    }], plotlyLayout({
      title: "Average Protection Score by region",
      height: 360, yaxis: { title: "Avg Protection (0–20)", range: [0, 20] }
    }), PLOT_CFG);
  }

  function renderRadar(Plotly, data, countryNames) {
    var node = el("sc-radar");
    if (!node) return;
    var inds = data.meta.indicators;
    var theta = inds.map(function (i) { return i.label; });
    var byName = {};
    data.countries.forEach(function (c) { byName[c.country] = c; });
    var traces = (countryNames || []).map(function (name) {
      var c = byName[name];
      if (!c) return null;
      var r = inds.map(function (i) { return c.scores[i.key] === null ? 0 : c.scores[i.key]; });
      r.push(r[0]); var th = theta.concat([theta[0]]);  // close the loop
      return { type: "scatterpolar", r: r, theta: th, fill: "toself", name: name };
    }).filter(Boolean);

    if (!traces.length) {
      Plotly.purge(node);
      node.innerHTML = '<p class="sc-hint">Select countries above to compare their indicator profiles.</p>';
      return;
    }
    node.innerHTML = "";  // clear the placeholder hint before plotting
    Plotly.newPlot(node, traces, plotlyLayout({
      title: "Indicator profile comparison (0–2 per indicator)",
      height: 480,
      polar: { radialaxis: { visible: true, range: [0, 2], dtick: 1 } },
      legend: { orientation: "h", y: -0.1 }
    }), PLOT_CFG);
  }

  /* ---------- sortable / filterable table ---------- */

  function fmt(v) { return (v === null || v === undefined) ? "—" : v; }

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function cell(score) {
    if (score === 0 || score === 1 || score === 2) {
      return '<td class="sc-cell" style="background:' + SCORE_COLORS[score] +
        '" title="' + SCORE_LABELS[score] + '">' + score + "</td>";
    }
    return '<td class="sc-cell sc-na" title="No data">–</td>';
  }

  function scoreChip(score) {
    if (score === 0 || score === 1 || score === 2) {
      return '<span class="sc-chip" style="background:' + SCORE_COLORS[score] + '">' + score + "</span>";
    }
    return '<span class="sc-chip sc-na-chip">n/a</span>';
  }

  function sourceLinks(src) {
    if (!src) return "";
    return src.split(/\s*;\s*/).filter(Boolean).map(function (s, i) {
      s = s.trim();
      if (/^https?:\/\//i.test(s)) {
        return '<a href="' + esc(s) + '" target="_blank" rel="noopener noreferrer">source' +
          (i ? " " + (i + 1) : "") + " ↗</a>";
      }
      return '<span class="sc-src-note">' + esc(s) + "</span>";
    }).join(" · ");
  }

  function buildTable(data, rows) {
    var inds = data.meta.indicators;
    var head = '<tr><th data-k="country">Country</th><th data-k="region">Region</th>';
    inds.forEach(function (i) {
      head += '<th class="sc-ind-h" data-k="' + i.key + '" title="' + esc(i.label) + '">' + i.key + "</th>";
    });
    head += '<th data-k="protection_score">Prot.</th><th data-k="risk_index">Risk</th>' +
      '<th data-k="documented" title="Indicators with a documented justification">Doc</th></tr>';

    var nInd = inds.length;
    var body = rows.map(function (c) {
      var tr = '<tr data-country="' + esc(c.country) + '"><td class="sc-country">' +
        esc(c.country) + "</td><td>" + esc(c.region || "—") + "</td>";
      inds.forEach(function (i) { tr += cell(c.scores[i.key]); });
      tr += '<td class="sc-num">' + fmt(c.protection_score) + "</td>";
      tr += '<td class="sc-num">' + fmt(c.risk_index) + "</td>";
      tr += '<td class="sc-num sc-doc' + (c.documented < nInd ? " sc-doc-warn" : "") + '">' +
        c.documented + "/" + nInd + "</td></tr>";
      return tr;
    }).join("");

    return '<div class="sc-table-wrap"><table class="sc-table"><thead>' + head +
      "</thead><tbody>" + body + "</tbody></table></div>";
  }

  /* ---------- country detail panel ---------- */

  function showDetail(data, countryName) {
    var host = el("sc-detail");
    if (!host) return;
    var c = null;
    for (var i = 0; i < data.countries.length; i++) {
      if (data.countries[i].country === countryName) { c = data.countries[i]; break; }
    }
    if (!c) return;
    var inds = data.meta.indicators;
    var gaps = inds.length - c.documented;

    var html = '<div class="sc-detail-card">' +
      '<button type="button" class="sc-detail-close" aria-label="Close">×</button>' +
      '<h3 class="no-rainbow">' + esc(c.country) + "</h3>" +
      '<p class="sc-detail-sub">' + esc(c.region || "—") +
      (c.region_specific ? " · " + esc(c.region_specific) : "") + "</p>" +
      '<div class="sc-detail-stats">' +
      "<span><strong>" + fmt(c.protection_score) + "</strong> / 20 Protection</span>" +
      "<span><strong>" + fmt(c.risk_index) + "</strong> / 100 Risk</span>" +
      '<span class="' + (gaps ? "sc-doc-warn" : "") + '"><strong>' + c.documented +
      "</strong> / " + inds.length + " documented</span></div>";
    if (gaps > 0) {
      html += '<p class="sc-detail-flag">⚠ ' + gaps + " indicator" + (gaps > 1 ? "s" : "") +
        " scored without a documented justification — interpret with caution while source validation is ongoing.</p>";
    }
    html += '<ul class="sc-detail-list">';
    inds.forEach(function (ind) {
      var sv = c.scores[ind.key];
      var txt = c.text[ind.key];
      var src = c.sources ? c.sources[ind.key] : null;
      var rule = (ind.rules && String(sv) in ind.rules) ? ind.rules[String(sv)] : "";
      html += "<li><div class=\"sc-detail-ind\">" + scoreChip(sv) +
        '<span class="sc-detail-label">' + esc(ind.label) +
        (rule ? ' <span class="sc-detail-rule">(' + esc(rule) + ")</span>" : "") + "</span></div>";
      html += '<div class="sc-detail-text">' +
        (txt ? esc(txt) : '<em class="sc-doc-warn">No documented assessment.</em>') + "</div>";
      if (src) html += '<div class="sc-detail-src">Sources: ' + sourceLinks(src) + "</div>";
      html += "</li>";
    });
    html += "</ul></div>";
    host.innerHTML = html;
    var close = host.querySelector(".sc-detail-close");
    if (close) close.onclick = function () { host.innerHTML = ""; };
    host.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function wireRowClicks(data) {
    document.querySelectorAll(".sc-table tbody tr").forEach(function (tr) {
      tr.style.cursor = "pointer";
      tr.onclick = function () {
        var name = tr.getAttribute("data-country");
        if (name) showDetail(data, name);
      };
    });
  }

  /* ---------- explorer controller ---------- */

  function initExplorer(data) {
    var root = el("sc-explorer");
    if (!root) return;

    var state = { region: "all", indicator: "all", minScore: 0, q: "", onlyDocumented: false };
    var nInd = data.meta.indicators.length;

    // Populate region & indicator selectors
    var regSel = el("sc-f-region");
    if (regSel && !regSel.dataset.ready) {
      data.meta.regions.forEach(function (r) {
        var o = document.createElement("option"); o.value = r; o.textContent = r; regSel.appendChild(o);
      });
      regSel.dataset.ready = "1";
    }
    var indSel = el("sc-f-indicator");
    if (indSel && !indSel.dataset.ready) {
      data.meta.indicators.forEach(function (i) {
        var o = document.createElement("option"); o.value = i.key; o.textContent = i.label; indSel.appendChild(o);
      });
      indSel.dataset.ready = "1";
    }
    var cmpSel = el("sc-compare");
    if (cmpSel && !cmpSel.dataset.ready) {
      data.countries.slice().sort(function (a, b) { return a.country.localeCompare(b.country); })
        .forEach(function (c) {
          var o = document.createElement("option"); o.value = c.country; o.textContent = c.country; cmpSel.appendChild(o);
        });
      cmpSel.dataset.ready = "1";
    }

    function apply() {
      var rows = data.countries.filter(function (c) {
        if (state.region !== "all" && c.region !== state.region) return false;
        if (state.q && c.country.toLowerCase().indexOf(state.q) < 0) return false;
        if (state.onlyDocumented && c.documented < nInd) return false;
        if (state.indicator !== "all") {
          var v = c.scores[state.indicator];
          if (v === null || v === undefined || v < state.minScore) return false;
        } else if (state.minScore > 0) {
          if (c.protection_score === null || c.protection_score < state.minScore) return false;
        }
        return true;
      });
      rows.sort(function (a, b) {
        return (b.protection_score || 0) - (a.protection_score || 0) || a.country.localeCompare(b.country);
      });
      var tableHost = el("sc-table");
      if (tableHost) tableHost.innerHTML = buildTable(data, rows);
      var count = el("sc-count");
      if (count) count.textContent = rows.length + " of " + data.countries.length + " countries";
      wireSort(data, rows);
      wireRowClicks(data);
    }

    function bind(id, ev, fn) { var n = el(id); if (n) n.addEventListener(ev, fn); }
    bind("sc-f-region", "change", function (e) { state.region = e.target.value; apply(); });
    bind("sc-f-indicator", "change", function (e) { state.indicator = e.target.value; apply(); });
    bind("sc-f-minscore", "input", function (e) {
      state.minScore = Number(e.target.value) || 0;
      var out = el("sc-f-minscore-val"); if (out) out.textContent = state.minScore;
      apply();
    });
    bind("sc-f-search", "input", function (e) { state.q = e.target.value.trim().toLowerCase(); apply(); });
    bind("sc-f-documented", "change", function (e) { state.onlyDocumented = e.target.checked; apply(); });
    bind("sc-f-reset", "click", function () {
      state = { region: "all", indicator: "all", minScore: 0, q: "", onlyDocumented: false };
      ["sc-f-region", "sc-f-indicator"].forEach(function (i) { var n = el(i); if (n) n.value = "all"; });
      var ms = el("sc-f-minscore"); if (ms) ms.value = 0;
      var msv = el("sc-f-minscore-val"); if (msv) msv.textContent = "0";
      var q = el("sc-f-search"); if (q) q.value = "";
      var dc = el("sc-f-documented"); if (dc) dc.checked = false;
      apply();
    });

    if (cmpSel) {
      cmpSel.addEventListener("change", function () {
        var chosen = Array.prototype.slice.call(cmpSel.selectedOptions).map(function (o) { return o.value; }).slice(0, 5);
        loadPlotly().then(function (P) { renderRadar(P, data, chosen); });
      });
    }

    apply();
  }

  // click-to-sort table headers
  function wireSort(data, rows) {
    var table = document.querySelector(".sc-table");
    if (!table) return;
    table.querySelectorAll("th").forEach(function (th) {
      th.style.cursor = "pointer";
      th.onclick = function () {
        var k = th.getAttribute("data-k");
        var asc = th.dataset.asc !== "1";
        th.dataset.asc = asc ? "1" : "0";
        var sorted = rows.slice().sort(function (a, b) {
          var av = (k in a) ? a[k] : a.scores[k];
          var bv = (k in b) ? b[k] : b.scores[k];
          if (av === null || av === undefined) av = -Infinity;
          if (bv === null || bv === undefined) bv = -Infinity;
          if (typeof av === "string") return asc ? av.localeCompare(bv) : bv.localeCompare(av);
          return asc ? av - bv : bv - av;
        });
        var host = el("sc-table");
        if (host) { host.innerHTML = buildTable(data, sorted); wireSort(data, sorted); wireRowClicks(data); }
      };
    });
  }

  /* ---------- entry point ---------- */

  function hasViz() {
    return el("sc-map") || el("sc-indicators") || el("sc-regions") ||
      el("sc-table") || el("sc-explorer") || el("sc-radar");
  }

  function init() {
    if (!hasViz()) return;  // not a scorecard viz page — stay inert
    var loading = el("sc-loading");
    loadData()
      .then(function (data) {
        // stamp metadata line if present
        var meta = el("sc-meta");
        if (meta) {
          meta.textContent = data.meta.country_count + " countries · " +
            data.meta.indicators.length + " indicators · source verified " +
            (data.meta.source_verified || "n/a").slice(0, 10);
        }
        // explorer is plain DOM/table — render even if Plotly fails
        initExplorer(data);
        var metricSel = el("sc-map-metric");
        return loadPlotly().then(function (P) {
          renderMap(P, data);
          renderIndicators(P, data);
          renderRegions(P, data);
          renderRadar(P, data, []);
          if (metricSel && !metricSel.dataset.ready) {
            metricSel.addEventListener("change", function () { renderMap(P, data); });
            metricSel.dataset.ready = "1";
          }
        });
      })
      .then(function () { if (loading) loading.style.display = "none"; })
      .catch(function (err) {
        console.error("Scorecard viz error:", err);
        if (loading) {
          loading.innerHTML = '<strong>Could not load the scorecard data.</strong> ' +
            "Please refresh, or view the data via the API / CSV exports.";
        }
      });
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);     // Material instant navigation
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
