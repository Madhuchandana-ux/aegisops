# External Dataset → AegisOps Mapping

## Source

Classification of IT Support Tickets

Source:
https://zenodo.org/records/7648117

DOI:
10.5281/zenodo.7648117

## Mapping

| AegisOps field | Source information | Transformation |
|---|---|---|
| incident_id | None | Generated unique ID |
| short_description | Ticket text | First 200 characters |
| description | Ticket text | Original text |
| category | Classification label | Direct mapping |
| subcategory | Not available | `unknown` |
| priority | Not available | `unknown` |
| impact | Not available | Null |
| urgency | Not available | Null |
| resolution | Not available | Empty |
| data_source | Dataset metadata | Constant identifier |

## Important

Unavailable fields are not artificially generated.

This prevents fabricated labels and preserves the distinction between
observed data and assumptions.