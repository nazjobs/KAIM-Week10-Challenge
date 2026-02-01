# Unified Data Schema Documentation

To solve the challenge of biased event modeling, we implemented a relational schema.

## 1. Schema Structure
The dataset (`ethiopia_fi_unified_data.csv`) consists of four distinct record types:

### A. Observations
Verified measurements from surveys or reports.
- **Fields:** `value_numeric`, `unit`, `source_name`.
- **Example:** "Account Ownership is 46% in 2021."

### B. Events
Neutral occurrences defined by time and category.
- **Fields:** `category` (policy, product_launch), `observation_date`.
- **Example:** "Telebirr Launch (May 2021)".
- **Note:** Events are **NOT** assigned to pillars directly to avoid bias.

### C. Impact Links
The "Edge" connecting an Event to a specific Pillar.
- **Fields:** `parent_id` (links to Event), `impact_estimate`, `lag_months`.
- **Logic:** Allows one event (Telebirr) to have multiple effects:
    1. Increase `ACCESS` (Lag: 12 months)
    2. Increase `USAGE` (Lag: 3 months)

## 2. Enrichment Strategy
See `data_enrichment_log.md` for the audit trail of all added records.
Key enrichments included:
- **Infrastructure:** Added 4G coverage data to correlate with usage.
- **Active Users:** Added M-Pesa 90-day active numbers to calculate the "Activity Gap".
