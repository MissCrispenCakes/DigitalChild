/* GRIMdata — Scorecard visualizations & data explorer
 *
 * Renders the Digital Rights Scorecard from the static dataset published at
 * /scorecard/data/scorecard.json (built by utils/build_scorecard_viz_data.py).
 *
 * Pure static: no API/server required. Plotly is loaded from CDN on demand,
 * only after the visitor explicitly enables charts on the current page. Designed to work
 * with Material for MkDocs "navigation.instant" via the document$ observable.
 */
(function () {
  "use strict";

  var PLOTLY_SRC = "https://cdn.plot.ly/plotly-2.27.0.min.js";

  // Score → colour (0 worst → 2 best). Used for table heatmap cells & bars.
  var SCORE_COLORS = { 0: "#a92f3b", 1: "#946000", 2: "#17633d" };
  var SCORE_LABELS = { 0: "0 — Worst", 1: "1 — Partial", 2: "2 — Best" };

  var _dataPromise = null;
  var _plotlyPromise = null;
  var _comparisonNames = [];

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
        s.onerror = function () { _plotlyPromise = null; s.remove(); reject(new Error("Failed to load Plotly")); };
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
    topojsonURL: "https://cdn.plot.ly/",
    modeBarButtonsToRemove: ["lasso2d", "select2d", "autoScale2d"] };

  /* ---------- charts ---------- */

  var GREEN_TO_RED = [[0, "#a92f3b"], [0.5, "#946000"], [1, "#17633d"]];
  var RED_TO_GREEN = [[0, "#17633d"], [0.5, "#946000"], [1, "#a92f3b"]];
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

    return Plotly.newPlot(node, [trace], plotlyLayout({
      title: "Digital Rights — " + cfg.title + " by Country",
      geo: { showframe: false, showcoastlines: false, projection: { type: "natural earth" }, bgcolor: "rgba(0,0,0,0)" },
      margin: { t: 40, r: 0, b: 0, l: 0 }, height: 460
    }), PLOT_CFG).then(function () {
      node.removeAllListeners("plotly_click");
      node.on("plotly_click", function (ev) {
        if (ev && ev.points && ev.points.length && ev.points[0].customdata) {
          showDetail(data, ev.points[0].customdata);
        }
      });
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
    return Plotly.newPlot(node, traces, plotlyLayout({
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

    return Plotly.newPlot(node, [{
      type: "bar",
      x: regions.map(function (r) { return r.region; }),
      y: regions.map(function (r) { return Math.round(r.avg * 10) / 10; }),
      marker: { color: regions.map(function (r) {
        var t = r.avg / 20; return t < 0.4 ? "#a92f3b" : t < 0.65 ? "#946000" : "#17633d"; }) },
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
      var r = inds.map(function (i) { return c.scores[i.key] == null ? null : c.scores[i.key]; });
      r.push(r[0]); var th = theta.concat([theta[0]]);  // close the loop
      return { type: "scatterpolar", r: r, theta: th, fill: "none", connectgaps: false, name: name };
    }).filter(Boolean);

    if (!traces.length) {
      Plotly.purge(node);
      node.innerHTML = '<p class="sc-hint">Select countries above to compare their indicator profiles.</p>';
      return;
    }
    node.innerHTML = "";  // clear the placeholder hint before plotting
    return Plotly.newPlot(node, traces, plotlyLayout({
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
        return '<a href="' + esc(s) + '" >source' +
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
        '<button type="button" class="sc-country-button">' + esc(c.country) + "</button></td><td>" + esc(c.region || "—") + "</td>";
      inds.forEach(function (i) { tr += cell(c.scores[i.key]); });
      tr += '<td class="sc-num">' + fmt(c.protection_score) + "</td>";
      tr += '<td class="sc-num">' + fmt(c.risk_index) + "</td>";
      tr += '<td class="sc-num sc-doc' + (c.documented < nInd ? " sc-doc-warn" : "") + '">' +
        c.documented + "/" + nInd + "</td></tr>";
      return tr;
    }).join("");

    head = head.replace(/<th([^>]*)>(.*?)<\/th>/g, function (_, attrs, label) {
      return '<th scope="col"' + attrs + '><button type="button" class="sc-sort" aria-label="Sort by ' +
        esc(label.replace(/<[^>]*>/g, "")) + '">' + label + '</button></th>';
    });
    return '<div class="sc-table-wrap" tabindex="0" role="region" aria-label="Country assessments; scroll to see all indicators"><table class="sc-table"><caption class="grim-sr-only">Digital rights scores and documented assessments. Use a country button for evidence.</caption><thead>' + head +
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

    var previousFocus = document.activeElement;
    var html = '<div class="sc-detail-card" role="region" aria-labelledby="sc-detail-title" tabindex="-1">' +
      '<button type="button" class="sc-detail-close" aria-label="Close country assessment">×</button>' +
      '<h3 id="sc-detail-title" class="no-rainbow">' + esc(c.country) + "</h3>" +
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
    if (close) close.onclick = function () {
      host.innerHTML = "";
      if (previousFocus && previousFocus.isConnected) previousFocus.focus({ preventScroll: true });
    };
    host.querySelector(".sc-detail-card").focus({ preventScroll: true });
    host.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "nearest" });
  }

  function wireRowClicks(data) {
    document.querySelectorAll(".sc-country-button").forEach(function (button) {
      button.onclick = function () {
        showDetail(data, button.closest("tr").getAttribute("data-country"));
      };
    });
  }

  /* ---------- explorer controller ---------- */

  function initExplorer(data) {
    var root = el("sc-explorer");
    if (!root || root.dataset.initialized) return;
    root.dataset.initialized = "1";
    var state = { region: "all", indicator: "all", minScore: 0, q: "", onlyDocumented: false,
      sortKey: "protection_score", ascending: false };
    var nInd = data.meta.indicators.length;
    var regSel = el("sc-f-region");
    var indSel = el("sc-f-indicator");
    var cmpSel = el("sc-compare");
    function option(select, value, label) {
      if (!select) return;
      var o = document.createElement("option"); o.value = value; o.textContent = label; select.appendChild(o);
    }
    data.meta.regions.forEach(function (v) { option(regSel, v, v); });
    data.meta.indicators.forEach(function (v) { option(indSel, v.key, v.label); });
    data.countries.slice().sort(function (a, b) { return a.country.localeCompare(b.country); })
      .forEach(function (c) { option(cmpSel, c.country, c.country); });
    _comparisonNames = [];

    function apply(focusKey) {
      var rows = data.countries.filter(function (c) {
        if (state.region !== "all" && c.region !== state.region) return false;
        if (state.q && c.country.toLowerCase().indexOf(state.q) < 0) return false;
        if (state.onlyDocumented && c.documented < nInd) return false;
        var v = state.indicator === "all" ? c.protection_score : c.scores[state.indicator];
        if (state.minScore > 0 && (v == null || v < state.minScore)) return false;
        if (state.indicator !== "all" && v == null) return false;
        return true;
      });
      rows.sort(function (a, b) {
        var k = state.sortKey, av = k in a ? a[k] : a.scores[k], bv = k in b ? b[k] : b.scores[k];
        if (av == null && bv == null) return a.country.localeCompare(b.country);
        if (av == null) return 1;
        if (bv == null) return -1;
        var cmp = typeof av === "string" ? String(av).localeCompare(String(bv)) : av - bv;
        return (state.ascending ? cmp : -cmp) || a.country.localeCompare(b.country);
      });
      var host = el("sc-table");
      if (host) host.innerHTML = buildTable(data, rows);
      var count = el("sc-count");
      if (count) count.textContent = rows.length + " of " + data.countries.length + " countries";
      if (!rows.length && host) host.insertAdjacentHTML("beforeend", '<p>No countries match. Try Reset or broaden the filters.</p>');
      document.querySelectorAll(".sc-table th[data-k]").forEach(function (th) {
        var k = th.getAttribute("data-k"), button = th.querySelector("button");
        th.setAttribute("aria-sort", k === state.sortKey ? (state.ascending ? "ascending" : "descending") : "none");
        if (k === state.sortKey) button.textContent += state.ascending ? " ↑" : " ↓";
        button.onclick = function () {
          state.ascending = state.sortKey === k ? !state.ascending : true;
          state.sortKey = k;
          apply(k);
        };
        if (focusKey === k) button.focus({ preventScroll: true });
      });
      wireRowClicks(data);
    }
    function bind(id, ev, fn) { var n = el(id); if (n) n.addEventListener(ev, fn); }
    function updateRange() {
      var range = el("sc-f-minscore");
      if (range) { range.max = state.indicator === "all" ? 20 : 2; range.value = state.minScore = 0; }
      var out = el("sc-f-minscore-val"); if (out) out.textContent = "0";
      var label = el("sc-f-minscore-label");
      if (label) label.textContent = state.indicator === "all" ? "Minimum Protection Score (0–20)" : "Minimum indicator score (0–2)";
    }
    bind("sc-f-region", "change", function (e) { state.region = e.target.value; apply(); });
    bind("sc-f-indicator", "change", function (e) { state.indicator = e.target.value; updateRange(); apply(); });
    bind("sc-f-minscore", "input", function (e) {
      state.minScore = Number(e.target.value) || 0;
      var out = el("sc-f-minscore-val"); if (out) out.textContent = state.minScore;
      apply();
    });
    bind("sc-f-search", "input", function (e) { state.q = e.target.value.trim().toLowerCase(); apply(); });
    bind("sc-f-documented", "change", function (e) { state.onlyDocumented = e.target.checked; apply(); });
    bind("sc-f-reset", "click", function () {
      state = { region: "all", indicator: "all", minScore: 0, q: "", onlyDocumented: false,
        sortKey: "protection_score", ascending: false };
      ["sc-f-region", "sc-f-indicator"].forEach(function (i) { var n = el(i); if (n) n.value = "all"; });
      var q = el("sc-f-search"); if (q) q.value = "";
      var dc = el("sc-f-documented"); if (dc) dc.checked = false;
      var detail = el("sc-detail"); if (detail) detail.innerHTML = "";
      updateRange(); apply();
    });
    function updateComparison() {
      var host = el("sc-selected"); if (!host) return;
      host.innerHTML = _comparisonNames.map(function (name) {
        return '<button type="button" class="md-button sc-remove" data-country="' + esc(name) + '" aria-label="Remove ' + esc(name) + ' from comparison">' + esc(name) + ' ×</button>';
      }).join(" ");
      host.querySelectorAll("button").forEach(function (button) {
        button.onclick = function () {
          _comparisonNames = _comparisonNames.filter(function (n) { return n !== button.dataset.country; });
          updateComparison();
          if (cmpSel) cmpSel.focus();
        };
      });
      var status = el("sc-compare-status");
      if (status) status.textContent = _comparisonNames.length + " of 5 countries selected. Missing values are gaps, not zero scores.";
      var gate = el("sc-chart-permission");
      if (gate && gate.dataset.enabled && window.Plotly) renderRadar(window.Plotly, data, _comparisonNames);
    }
    bind("sc-compare-add", "click", function () {
      if (!cmpSel || !cmpSel.value) return;
      if (_comparisonNames.indexOf(cmpSel.value) >= 0) {
        el("sc-compare-status").textContent = "That country is already selected."; return;
      }
      if (_comparisonNames.length >= 5) {
        el("sc-compare-status").textContent = "Five countries are selected. Remove one before adding another."; return;
      }
      _comparisonNames.push(cmpSel.value); updateComparison();
    });
    updateRange(); updateComparison(); apply();
  }

  /* ---------- entry point ---------- */

  function hasViz() {
    return el("sc-map") || el("sc-indicators") || el("sc-regions") ||
      el("sc-table") || el("sc-explorer") || el("sc-radar");
  }

  function renderCharts(data) {
    var P = window.Plotly;
    return Promise.all([renderMap(P, data), renderIndicators(P, data), renderRegions(P, data),
      renderRadar(P, data, _comparisonNames)]);
  }

  function init() {
    if (!hasViz()) return;
    var loading = el("sc-loading"), gate = el("sc-chart-permission");
    loadData().then(function (data) {
      // Ignore a fetch finishing after its page has been replaced by instant navigation.
      if (loading && !loading.isConnected) return;
      var meta = el("sc-meta");
      if (meta) meta.textContent = data.meta.country_count + " countries · " + data.meta.indicators.length +
        " indicators · snapshot " + data.meta.generated_at.slice(0, 10) +
        " · source-verification stamp " + (data.meta.source_verified || "n/a").slice(0, 10);
      initExplorer(data);
      if (loading) loading.hidden = true;
      if (!gate || gate.dataset.initialized) return;
      gate.dataset.initialized = "1";
      var button = el("sc-load-charts"), status = el("sc-chart-status");
      button.onclick = function () {
        button.disabled = true; status.textContent = "Loading external chart assets…";
        loadPlotly().then(function () {
          if (!gate.isConnected) return;
          gate.dataset.enabled = "1";
          return renderCharts(data);
        }).then(function () {
          if (!gate.isConnected) return;
          status.textContent = "Charts enabled on this page. The country table and downloads remain available.";
          button.hidden = true;
        }).catch(function () {
          delete gate.dataset.enabled;
          status.textContent = "Charts could not load. The table and published downloads still work. You can retry.";
          button.disabled = false;
        });
      };
      var metric = el("sc-map-metric");
      if (metric) metric.onchange = function () {
        if (gate.dataset.enabled) renderMap(window.Plotly, data).catch(function () {
          status.textContent = "Map assets could not load. Use the country explorer or downloads.";
        });
      };
    }).catch(function () {
      if (loading && loading.isConnected) loading.textContent = "Could not load the scorecard snapshot. Please refresh or use the published JSON/CSV downloads.";
    });
  }

  // Chart colours follow the actual current appearance, including instant navigation.
  new MutationObserver(function () {
    var gate = el("sc-chart-permission");
    if (gate && gate.dataset.enabled && window.Plotly) {
      loadData().then(renderCharts).catch(function () {});
    }
  }).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
