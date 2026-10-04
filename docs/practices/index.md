# Site practices & participation

[← GRIMdata Home](../index.md){ .md-button }

Browse the research freely, choose whether to load external charts, and see how sources and contributions are handled.

## Public browsing and understandable choices

You can read the research, search documentation, filter the country table, and explore Source Transparency Watch without an account. GRIMdata does not use analytics scripts or collect visitor submissions through this site.

The table and watch tools fetch published JSON from this site's origin. Filtering and searching those tools happen in your browser. Documentation search uses a same-origin index and browser worker. A shared search link may contain your query in its URL; that query can be visible in browser history and to anyone you share the link with.

Your browser stores your appearance preferences locally. The hosting provider may receive request information such as your IP address; we have not verified its logging or retention practices.

## Optional external charts

The table works without external charts. Selecting **Load interactive charts** requests Plotly from `cdn.plot.ly`; the world map also requests geographic assets from that provider. The provider receives normal request information. No country search terms or uploaded personal data are sent by GRIMdata's chart code.

Charts stay off until you choose to load them. That choice lasts for the current page; navigating to another chart page or reloading asks you to choose again.

Links to publications, project sites, and GitHub take you to external services with their own privacy practices. Links open normally unless labelled as opening a new tab.

## Provenance, uncertainty, and attribution

The published visualization snapshot was generated **26 June 2026** from `Global_QueerAI_Child_Scorecard_MASTER.xlsx`. Its metadata records source verification on **9 September 2025**. These dates have different meanings; source reachability does not establish substantive accuracy or present-day legal status.

Scores are screening signals. Inspect written justifications, original sources, and the [methodology](../scorecard/design.md). Missing values remain missing in comparisons. Cite the version/date and relevant sources, state documentation gaps, and pair numerical comparisons with contextual research.

The [software citation](../docs/technical-overview.md#citation) and [project publications](../website/projects/index.md#publications) identify the research record. Code uses the MIT licence; the project's data and documentation use CC BY 4.0. Original third-party documents retain their own terms. See [data governance](../DATA_GOVERNANCE.md).

## Contributing {#contributing-and-future-participation}

[Suggest a correction on GitHub](https://github.com/MissCrispenCakes/DigitalChild/issues). Include the country, indicator, proposed correction, and a public authoritative source. GitHub issues are public, so keep personal or confidential information out of your report.

For code, documentation, or data contributions, read the [contributing guide](../CONTRIBUTING.md) and its licensing terms. Contributions become part of the project's public history; earlier versions and downloaded copies may remain available after a correction. Raise any attribution questions before contributing.
