# Open Data AI Analytics  
## Laboratory Work: Version Control and Open Data Analysis

---

## Project Overview

This laboratory work demonstrates the use of Git version control practices within a structured data analytics project. The goal is to organize a small analytical workflow using open data, implement modular development through feature branches, and apply basic data analysis techniques.

The project follows a staged development process:

- Data loading
- Data quality analysis
- Exploratory data research
- Data visualization
- Merge conflict simulation and resolution
- Release versioning

The focus is not only on analysis itself, but on proper project structure, branching strategy, and clean repository management.

---

## Dataset Description

The project is based on open data related to **electronic petitions submitted to public authorities in Ukraine**.

Open Data Source:  
https://data.gov.ua/dataset/8e2a1cc8-20e3-49f1-b9bf-b1c0372f4834

The dataset contains structured information about petitions, including submission dates, number of collected signatures, required thresholds, and status.

---

## Development Workflow

The project was implemented using a feature-branch workflow:

- `feature/data_load`
- `feature/data_quality_analysis`
- `feature/data_research`
- `feature/visualization`

Each feature was developed in a separate branch and merged into `main` via pull/merge requests. A controlled merge conflict was intentionally created and resolved to demonstrate Git conflict management.

---

## Tools Used

- Python
- Pandas
- Matplotlib / Seaborn (for visualization)
- Git (branching, merging, tagging)

---

## Release

Version `v0.1.0` marks the completion of the laboratory work, including analysis modules, documentation, and changelog.
