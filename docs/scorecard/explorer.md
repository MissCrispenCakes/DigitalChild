# Data Explorer

Interactive exploration of scorecard data (coming soon).

!!! info "Under Development"
    The data explorer is currently under development. This page will feature:
    ```txt
    - Filter by country, region, or indicator
    - Sort and search capabilities
    - Export filtered results
    - Compare multiple countries side-by-side
    ```

## Current Options

While the interactive explorer is being built, you can explore the data through:

### 1. CSV Exports

Export scorecard data to CSV:

```bash
python pipeline_runner.py --mode scorecard --scorecard-action export
```

Then analyze with your preferred tool:

- **Excel/Google Sheets** - Pivot tables and charts
- **Python pandas** - Programmatic analysis
- **R** - Statistical analysis
- **Tableau/Power BI** - Advanced visualizations

### 2. Direct File Access

Scorecard data is stored in:

```txt
scorecard_main.xlsx
```

Open directly in Excel to view raw data with all 10 indicators across 194 countries.

### 3. Python Analysis

Quick analysis with pandas:

```python
import pandas as pd

# Load scorecard data
df = pd.read_excel('scorecard_main.xlsx', sheet_name='Indicators')

# Filter by region
africa = df[df['Region'] == 'Africa']

# Count by indicator value
ai_policy_counts = df['AI_Policy_Status'].value_counts()
print(ai_policy_counts)

# Countries with comprehensive data protection
data_protection = df[df['Data_Protection_Law'] == 'Comprehensive Law']
print(data_protection[['Country', 'Region']])
```

### 4. Metadata JSON

Enriched document metadata includes scorecard data:

```python
import json

with open('data/metadata/metadata.json', 'r') as f:
    metadata = json.load(f)

# Find documents with scorecard enrichment
for doc in metadata['documents']:
    if 'scorecard' in doc:
        print(f"{doc['id']}: {doc['scorecard']['matched_country']}")
```

## Planned Features

The data explorer will include:

### Filters

- **Country** - Select single or multiple countries
- **Region** - Africa, Americas, Asia, Europe, Oceania
- **Indicator** - Filter by specific indicators
- **Value** - Filter by indicator values

### Visualizations

- **Table View** - Sortable, searchable data table
- **Chart View** - Bar charts, pie charts, treemaps
- **Map View** - Choropleth maps showing global distribution
- **Comparison View** - Side-by-side country comparison

### Export Options

- **CSV** - Filtered results as CSV
- **JSON** - Structured data export
- **PDF** - Printable report
- **Image** - Export charts as PNG

## Development Timeline

See [Roadmap](../ROADMAP.md) for detailed timeline.

- **Phase 3 (Current):** CSV exports and basic visualization
- **Phase 4 (2026):** Interactive dashboard with filters
- **Phase 5 (2027):** Advanced analytics and comparisons

## Contribute

Want to help build the data explorer?

1. Check [open issues](https://github.com/MissCrispenCakes/DigitalChild/issues?q=is%3Aissue+is%3Aopen+label%3Avisualization)
1. Review [contribution guidelines](../CONTRIBUTING.md)
1. Submit pull requests with visualization improvements

Technologies we're considering:

- **Plotly.js** - Interactive charts
- **Dash** - Python dashboard framework
- **D3.js** - Custom visualizations
- **React** - Frontend framework

## Temporary Workaround

Until the explorer is ready, use this Python script for quick exploration:

```python
import pandas as pd

def explore_scorecard():
    """Interactive scorecard exploration."""
    df = pd.read_excel('scorecard_main.xlsx', sheet_name='Indicators')

    print("Available columns:")
    print(df.columns.tolist())

    while True:
        print("\n=== Scorecard Explorer ===")
        print("1. View country")
        print("2. View indicator")
        print("3. View region")
        print("4. Export filtered data")
        print("5. Exit")

        choice = input("Select option: ")

        if choice == '1':
            country = input("Enter country name: ")
            result = df[df['Country'] == country]
            print(result.T)  # Transpose for readability

        elif choice == '2':
            indicator = input("Enter indicator name: ")
            if indicator in df.columns:
                print(df[['Country', indicator]])
            else:
                print("Indicator not found")

        elif choice == '3':
            region = input("Enter region: ")
            result = df[df['Region'] == region]
            print(result[['Country', 'AI_Policy_Status', 'Data_Protection_Law']])

        elif choice == '4':
            filename = input("Export filename (e.g., filtered.csv): ")
            # Apply your filters here
            df.to_csv(filename, index=False)
            print(f"Exported to {filename}")

        elif choice == '5':
            break

if __name__ == '__main__':
    explore_scorecard()
```

Save as `explore_scorecard.py` and run:

```bash
python explore_scorecard.py
```

## Questions?

- [FAQ](../FAQ/)
- [Scorecard Workflow Guide](../guides/SCORECARD_WORKFLOW.md)
- [GitHub Discussions](https://github.com/MissCrispenCakes/DigitalChild/discussions)

______________________________________________________________________

Check back soon for the interactive data explorer! [Watch this repo](https://github.com/MissCrispenCakes/DigitalChild) for updates.
