# Exoplanet Analytics Dashboard
 
[Live Demo](https://nasa-exoplanet-etl-dashboard-0.streamlit.app/)
 
## Overview
An end-to-end ETL pipeline and interactive analytics dashboard built on real NASA exoplanet data.
Extracts live data from the NASA Exoplanet Archive API, stores it in a local SQLite database, and visualizes discovery trends through an interactive Streamlit dashboard.
 
Built to develop real data engineering skills using a real-world NASA data source.
 
## What It Does
- Extracts confirmed exoplanet records from the NASA Exoplanet Archive TAP API
- Filters 40,000+ parameter-set rows to one default record per planet via default_flag = 1
- Transforms raw JSON responses into structured, typed records
- Validates records by dropping nameless entries, clearing implausible discovery years while keeping the record, and deduplicating by planet name
- Loads 6,300+ unique exoplanet records into a SQLite database
- Displays total confirmed exoplanets, total confirmed host stars, and recently discovered exoplanet as KPI metrics
- Visualizes exoplanets discovered by facility and year, with discovery method shares as KPI tiles
- Implements structured error handling and logging across the ETL pipeline and analytics layer
- Automatically re-runs the pipeline on page load when the local database is more than a day old

## Data Pipeline Architecture
![Exoplanet ETL Pipeline Architecture](images/exoplanet-etl-pipeline-architecture(dark).drawio.png)
 
## Project Structure
```
nasa-exoplanet-etl-dashboard/
├── .streamlit/
│   └── config.toml
├── assets/
│   └── styles.css
├── src/
│   ├── etl.py
│   ├── analytics.py
│   └── pipeline.py
├── tests/
│   └── test_etl.py
├── images/
│   ├── star-background.jpg
│   └── exoplanet-etl-pipeline-architecture(dark).drawio.png
├── app.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Tech Stack
| Tool | Purpose |
|------|---------|
| Python | Core language |
| Requests | API extraction |
| Pandas | Data transformation |
| SQLite | Local data storage |
| Streamlit | Dashboard interface |
| Plotly | Interactive charts |
| Python logging | Error handling and pipeline logging |
 
## Getting Started
 
Install dependencies:
```
pip install -r requirements.txt
```
 
Run the ETL pipeline to populate the database:
```
python -m src.pipeline
```
> The dashboard will also run the pipeline automatically on first launch if this step is skipped.
 
Launch the dashboard:
```
streamlit run app.py
```

No API key required — the NASA Exoplanet Archive is fully public.

## Testing

Install development dependencies:
```
pip install -r requirements-dev.txt
```

Run the test suite from the project root:
```
python -m pytest
```

Use `python -m pytest` rather than bare `pytest` — the `-m` form puts the project
root on the import path so `src` resolves.

9 unit tests cover the transform and validate stages: field mapping, whitespace
and blank handling, numeric coercion, null-name removal, implausible-year
clearing, and duplicate collapsing.

 
## Features
- Live data pulled from the NASA Exoplanet Archive Planetary Systems table
- Total confirmed exoplanets, confirmed host stars, and recent discovery as KPI metrics
- Line chart showing planetary discovery trends over time (including the Kepler mission spike)
- Bar chart showing confirmed exoplanet discovery counts by top 10 discovery facility
- Top four discovery methods shown as KPI tiles with each method's share of all confirmed exoplanets, computed live in SQL
- Hover definitions explaining how each detection method works
- Analytical insight beneath the discovery timeline interpreting the 2014 and 2016 Kepler data releases
- Fully transparent charts over a space-themed background
- Data last retrieved timestamp displayed on dashboard

## What I Learned
- Building a modular ETL pipeline with separation of concerns across extract, transform, and load
- Querying a TAP (Table Access Protocol) compliant API using ADQL
- Persisting and querying structured data with SQLite
- Building an analytics layer with SQL aggregations on top of a database
- Translating raw data visualizations into domain-specific insights using NASA exoplanet science context
- Data storytelling through interactive Plotly visualizations in Streamlit
- Implementing structured logging with Python's logging module across a multi-module project

## Data Source
NASA Exoplanet Archive TAP API — Planetary Systems table (ps), maintained by Caltech/IPAC on behalf of NASA.
Fields extracted: pl_name, hostname, disc_year, disc_pubdate, discoverymethod, disc_facility