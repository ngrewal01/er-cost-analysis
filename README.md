# What Does an ER Visit Really Cost?

Analyzing U.S. emergency room costs by medical condition using MEPS 2023 —
the Medical Expenditure Panel Survey from AHRQ (Agency for Healthcare
Research and Quality).

**Research questions**

1. What does an ER visit cost on average, and how does that vary by condition?
2. Which conditions send people to the ER most often, and which are the most expensive?
3. How do costs differ by insurance coverage, age group, and U.S. region?
4. How big is the gap between what hospitals *charge* and what actually gets *paid*?

## Why MEPS?

MEPS is a nationally representative household survey. Unlike hospital
"chargemaster" data, it records what was **actually paid** for each visit
(by insurers + patients), not the inflated sticker price. Each row is one
real ER visit, linkable to the patient's conditions, demographics, and
insurance — which makes it ideal for this analysis, and it's free.

Trade-off to be aware of: it's a survey (~20k households/year), so we use
**survey weights** to produce national estimates, and rare conditions have
too few visits to estimate reliably.

## Data files (2023, the most recent year with all companion files)

| File | What it contains | Key columns |
|------|------------------|-------------|
| [HC-248E](https://meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-248E) ER Visits | One row per ER visit, with payments & charges | `ERXP23X` (paid), `ERTC23X` (charged), `EVNTIDX`, `PERWT23F` |
| [HC-249](https://meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-249) Medical Conditions | One row per reported condition | `CONDIDX`, `ICD10CDX`, `CCSR1X` (condition category) |
| [HC-248I](https://meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-248I) Condition–Event Link | Bridge table: which condition caused which visit | `CONDIDX` ↔ `EVNTIDX` |
| [HC-251](https://meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-251) Full-Year Consolidated | One row per person: demographics & insurance | `DUPERSID`, `AGELAST`, `INSCOV23`, `REGION23` |

Conditions are grouped using **CCSR** (Clinical Classifications Software
Refined) categories — AHRQ's standard grouping of ICD-10 diagnosis codes
into ~540 clinically meaningful buckets like "Abdominal pain" or
"Skin and subcutaneous tissue infections".

## Setup

```bash
# 1. Create and activate a virtual environment (keeps packages isolated to this project)
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the data (~25 MB total, straight from AHRQ)
python scripts/download_data.py

# 4. Open the notebook
jupyter lab notebooks/er_cost_analysis.ipynb   # or open in VSCode
```

## Project structure

```
er-cost-analysis/
├── README.md
├── requirements.txt
├── scripts/
│   └── download_data.py      # downloads & unzips all MEPS files
├── data/
│   ├── raw/                  # downloaded MEPS files (git-ignored)
│   └── processed/            # cleaned analysis table (git-ignored)
├── notebooks/
│   └── er_cost_analysis.ipynb
└── reports/
    └── figures/              # exported charts for the portfolio write-up
```

## Method notes (the honest fine print)

- **Survey weights.** Every average uses `PERWT23F` so estimates represent
  the U.S. civilian population, not just the survey sample.
- **Charges vs. payments.** `ERTC23X` is what the hospital billed;
  `ERXP23X` is what was actually paid. We analyze payments and show the
  gap explicitly.
- **Multi-condition visits.** One visit can be linked to several
  conditions; in per-condition stats a visit counts once under each of its
  conditions.
- **Small cells.** Conditions with fewer than 50 sampled visits are
  excluded from per-condition rankings (too noisy).
- **Simplification.** Proper standard errors for a complex survey need the
  design variables (`VARSTR`/`VARPSU`); this project reports weighted point
  estimates only and says so.

## Roadmap

- [x] Phase 0 — pick data source, scaffold project
- [x] Phase 1 — download data, load & explore each file
- [x] Phase 2 — merge into one visit-level analysis table
- [x] Phase 3 — analysis: averages by condition, payer, age, region
- [x] Phase 4 — polish charts, export figures
- [ ] Phase 5 — showcase: push to GitHub, write Squarespace post with key
      charts + link to the notebook

## Data citation

Agency for Healthcare Research and Quality. *Medical Expenditure Panel
Survey, 2023 Full Year Files.* AHRQ, Rockville, MD.
https://meps.ahrq.gov/
