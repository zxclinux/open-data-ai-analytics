## Laboratory Report: Open Data AI Analytics

### 1. Introduction

This laboratory work demonstrates a complete, but compact, analytics workflow on open government data using Git and Python.
The main goal is to analyse electronic petitions submitted to public authorities in Ukraine and to explore measurable patterns
in public engagement, signature dynamics, and petition outcomes.

### 2. Dataset

- **Source**: Open Data Portal of Ukraine (`https://data.gov.ua/dataset/8e2a1cc8-20e3-49f1-b9bf-b1c0372f4834`)
- **Entity**: electronic petitions to local public authorities
- **Key fields** (used in the analysis):
  - `uid` – petition identifier
  - `kind` – petition category
  - `title` – short description
  - `DateStartPetition` – petition start date
  - `count` – number of collected signatures
  - `status` – outcome / current status
  - `answerDate` – date of official response (if any)

The raw CSV file is stored in `data/raw/petitions.csv` and is downloaded via the `data_load.py` pipeline.

### 3. Research Questions

1. What is the distribution of collected signatures across petitions?
2. Does the duration until response relate to the number of signatures?
3. What percentage of petitions receive an official answer and how does this vary by category?
4. How has petition activity and support changed over time?

### 4. Methods and Pipelines

The project follows a simple, script-based pipeline architecture under `src/pipelines/`:

- `data_load.py` – downloads the raw CSV file into `data/raw/`.
- `data_quality_analysis.py` – prints basic descriptive statistics by counts, dates, categories, and statuses.
- `data_research.py` – performs deeper numeric analysis (percentiles, durations, signatures by category, success rates).
- `visualization.py` – generates figures under `reports/figures/` for distributions, medians, activity by year, and outcomes.

The analysis is implemented using `pandas` for data manipulation and `matplotlib` for visualizations.

### 5. Main Findings

- **Signatures distribution**: the distribution of signatures is highly skewed. Most petitions collect relatively few signatures,
  while a small number of petitions accumulate a high count, which confirms a long‑tail pattern of public support.
- **Petition duration and answers**: for petitions with an official response, the number of days between start and answer varies
  widely. The correlation between signature count and response time is weak, suggesting that response timing is not driven
  only by the number of signatures.
- **Differences by category**: categories such as housing/municipal services and city infrastructure tend to accumulate more
  signatures on average and show higher medians, indicating stronger public interest in everyday urban issues.
- **Success / answer rate**: only a fraction of petitions receive the status “answered”. Success rates vary across categories,
  which may reflect different policy priorities or feasibility of the proposed actions.
- **Dynamics over time**: the yearly breakdown of petitions and signatures shows that activity is not constant – some periods
  have noticeably more petitions and higher average support, which may correlate with local political or socio‑economic events.

These findings are summarized visually in the generated figures (`signatures_dist.png`, `median_by_kind.png`,
`mean_median_by_kind.png`, `activity_by_year.png`, `duration_dist.png`, `status_pie.png`).

### 6. Reproducibility

All steps are kept as simple scripts to follow the KISS principle and to be easily reproducible:

1. Download data  
   `python -m src.pipelines.data_load <DIRECT_CSV_URL>`
2. Run basic statistics  
   `python -m src.pipelines.data_quality_analysis`
3. Run deeper analytical summary  
   `python -m src.pipelines.data_research`
4. Generate visualizations  
   `python -m src.pipelines.visualization`

The repository is managed with Git and uses feature branches per pipeline, which makes the evolution of the analysis and
conflict resolution traceable through commit history and the accompanying `CHANGELOG.md`.

