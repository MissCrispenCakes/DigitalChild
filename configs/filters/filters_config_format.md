# Filters Config Format

## Fields

- region: filter by continent/region name (string or null)
- country: filter by country name (string or null)
- tags: list of required tags (array or null)

## Example

{
  "filters": {
    "region": "Africa",
    "country": "Kenya",
    "tags": ["ChildRights", "LGBTQ"]
  }
}
