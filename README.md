# Financial Inclusion Forecasting: Ethiopia (Interim 1)

**10 Academy - Artificial Intelligence Mastery (Week 10 Challenge)**

This project aims to build a forecasting system that tracks and predicts Ethiopia's digital financial transformation (2025-2027). It utilizes a **Unified Data Schema** to model how specific events (policy reforms, product launches like Telebirr/M-Pesa) impact financial inclusion metrics (Access & Usage).

## 📌 Project Status: Interim 1 Completed
- **Task 1:** Data Enrichment & Unified Schema Implementation ✅
- **Task 2:** Exploratory Data Analysis (EDA) & Visualization ✅
- **Next:** Event Impact Modeling & Forecasting (Tasks 3 & 4)

---

## 📂 Repository Structure

```
├── data/
│   └── raw/
│       ├── ethiopia_fi_unified_data.csv  # The "Source of Truth" dataset (Schema v2)
│       └── reference_codes.csv           # Valid codes for pillars/indicators
├── notebooks/
│   └── run_eda.py                        # Script to generate Task 2 visualizations
├── reports/
│   ├── figures/                          # Generated plots (Access Trend, Gender Gap, etc.)
│   └── interim_report.md                 # 📄 KEY INSIGHTS & DATA ANALYSIS REPORT
├── src/
│   └── data.py                           # Data loader & enrichment logic
├── generate_data.py                      # Utility to reconstruct the dataset from source
└── requirements.txt                      # Project dependencies
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone the repo
git clone https://github.com/nazjobs/KAIM-Week10-Challenge.git
cd KAIM-Week10-Challenge

# Create virtual environment (if not already active)
python -m venv .venv
source .venv/bin/activate.fish  # or .bash

# Install dependencies
pip install -r requirements.txt
```

### 2. Reproduce Data & Analysis
The raw data is already included in `data/raw`, but you can regenerate it or run the analysis script to reproduce the figures.

```bash
# Run the Exploratory Data Analysis (Task 2)
# This generates plots in reports/figures/
python notebooks/run_eda.py
```

---

## 📊 Methodology (Task 1)

### The Unified Schema
We moved away from hard-coding events to specific "Pillars". Instead, we use a relational approach:
1.  **Observations:** Raw Findex/NBE data points.
2.  **Events:** Neutral entities (e.g., "Telebirr Launch") defined by date and type.
3.  **Impact Links:** Explicit connections linking an **Event** to a **Pillar** (e.g., Telebirr → USAGE).

This allows a single event to impact multiple dimensions (e.g., `ACC_OWNERSHIP` and `GEN_GAP_ACC`) without duplicating event rows.

---

## 📈 Key Insights (Task 2)
*Full analysis available in [reports/interim_report.md](reports/interim_report.md)*

1.  **The Access-Usage Paradox:** While Account Ownership has slowed (46% → 49%), **Usage** (Digital Payments) has skyrocketed, driven by mobile money.
2.  **Infrastructure as a Leading Indicator:** 4G Coverage expansion (37% → 70%) strongly correlates with the recent spike in transaction volumes.
3.  **Persistent Gender Gap:** Despite new entrants, the gender gap in account ownership remains stagnant at ~18-20%, suggesting structural barriers persist.

---

## 🛠️ Tech Stack
- **Python 3.13**
- **Pandas:** Data manipulation & Time-series handling.
- **Seaborn/Matplotlib:** Visualization.
- **Git:** Atomic version control.

---
*Author: Nazrawi*
