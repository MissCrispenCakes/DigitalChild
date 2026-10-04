# Site practices & participation

[← GRIMdata Home](../index.md){ .md-button }

These statements describe the site's configured behaviour and reviewed custom code. They are not a guarantee about hosting-provider logs or every external service.

## Public browsing and understandable choices

You can read the research, search documentation, filter the country table, and inspect Source Transparency Watch without a GRIMdata account. No analytics script, visitor submission form, or upload feature is configured in this site.

The table and watch tools fetch published JSON from this site's origin. Filtering and searching those tools happen in your browser. Documentation search uses a same-origin index and browser worker. A shared search link may contain your query in its URL; that query can be visible in browser history and to anyone you share the link with.

The theme stores appearance preferences in browser local storage. Those preferences are not a research submission. Hosting providers may receive ordinary request information such as an IP address; their logging and retention practices have not been verified in this review.

## Optional external charts

The table works without external charts. Selecting **Load interactive charts** requests Plotly from `cdn.plot.ly`; the world map also requests geographic assets from that provider. The provider receives normal request information. No country search terms or uploaded personal data are sent by GRIMdata's chart code.

This choice applies only to the current page. Navigating to another chart page requires another choice. There is no stored chart-consent preference. Reloading does not automatically enable the charts. Once an external request has occurred, leaving the page cannot undo it.

The site uses system fonts, bundled SVG icons, browser-native emoji text, and text DOI links. The repository header is a static link and does not automatically fetch GitHub statistics. Links to publications, project splash sites, and GitHub take you to external services with their own practices. Links open normally unless explicitly labelled as opening a new tab.

## Provenance, uncertainty, and attribution

The published visualization snapshot was generated **26 June 2026** from `Global_QueerAI_Child_Scorecard_MASTER.xlsx`. Its metadata records source verification on **9 September 2025**. These dates have different meanings; source reachability does not establish substantive accuracy or present-day legal status.

Scores are screening signals. Inspect written justifications, original sources, and the [methodology](../scorecard/design.md). Missing values remain missing in comparisons. Cite the version/date and relevant sources, state documentation gaps, and pair numerical comparisons with contextual research.

The [software citation](../docs/technical-overview.md#citation) and [project publications](../website/projects/index.md#publications) identify the research record. Code uses the MIT licence; the project's data and documentation use CC BY 4.0. Original third-party documents retain their own terms. See [data governance](../DATA_GOVERNANCE.md).

## Contributing and future participation

[GitHub issues and discussions](https://github.com/MissCrispenCakes/DigitalChild/issues) are external and may be public. Do not post personal, confidential, or sensitive information there. For a data correction, provide the country, indicator, proposed correction, and a public authoritative source; follow the [contributing guidance](../CONTRIBUTING.md).

A contribution may enter a versioned public record and be attributed according to the project's contribution and licensing terms. Corrections or removal from future versions cannot guarantee removal from Git history, archives, citations, or copies already downloaded. Discuss attribution needs before submitting material.

Planned community or participant research requires its own understandable terms for scope, recording, attribution, reuse, and withdrawal before collecting contributions. No participant recruitment or informed-consent process is claimed to be operating through this website. EthicalCarbon is a separate resident-led community group; its future participation arrangements should be described by that group.
