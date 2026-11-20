# StreamVault Film Licensing Analysis

## 1. Project Overview

This project evaluates franchise collections and standalone films to support StreamVault's licensing decisions under a proposed **$14 million budget**.

It retrieves movie details and credits from TMDb, analyses historical financial performance, audience ratings, popularity and talent indicators, and produces candidate rankings and shortlists.

Two release-year windows are evaluated:

- **All years:** All eligible films in the supplied dataset.
- **2000 onward:** Eligible films released from 2000 onward.

The results support commercial investigation. They do not predict guaranteed streaming returns or establish licensing profitability.

## 2. Project Structure

```text
StreamVault-Analysis/
|-- data/
|   |-- raw/
|   |-- processed/
|   |-- quarantine/
|-- decision/
|   |-- ADR-001-data-source-and-quality.md
|   |-- ADR-002-franchise-classification.md
|   |-- ADR-003-financial-metrics-and-time-windows.md
|   |-- ADR-004-candidate-ranking-methodology.md
|-- outputs/
|-- src/
|-- .env.example
|-- .gitignore
|-- client_memo.md
|-- config.py
|-- data_findings.md
|-- id_list.csv
|-- main.py
|-- questions.md
|-- recommendation.md
|-- requirements.txt
|-- README.md
```

## 3. Requirements

- Python 3.10 or later.
- A TMDb API v4 Read Access Token.
- Internet connection for live data acquisition.
- Git for cloning the repository.

## 4. Setup Instructions

### Step 1: Clone the repository

```powershell
git clone <repository-url>
cd StreamVault-Analysis
```

Replace `<repository-url>` with the actual GitHub repository URL.

### Step 2: Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Configure the TMDb API token

Create a `.env` file in the project root.

Use `.env.example` as a guide and add your own TMDb v4 Read Access Token:

```env
TMDB_ACCESS_TOKEN=your_tmdb_access_token
```

Keep `.env` private. It must not be committed to GitHub.

## 5. Input Data

The project uses `id_list.csv` as its movie input file.

The CSV must contain a column named:

```text
tmdb_id
```

Each row should contain one TMDb movie identifier.

To analyse a different candidate list, replace the contents of `id_list.csv` while preserving the required column name.

The pipeline audits duplicate, invalid and missing identifiers. Unavailable titles are recorded rather than silently treated as successful retrievals.

The original supplied file contained 126 rows, although the brief referred to 127 identifiers.

## 6. Running the Analysis

From the project root, with the virtual environment activated, run:

```powershell
python main.py
```

The main script runs the complete analysis in the following order:

1. Retrieve movie details and credits from TMDb.
2. Prepare and process the retrieved data.
3. Validate data quality.
4. Engineer financial and analytical metrics.
5. Compare franchise and standalone performance.
6. Analyse candidate performance.
7. Analyse lead actors and directors.
8. Generate final rankings and shortlists.

The pipeline creates or refreshes the raw, processed, quarantined and output files.

No manual editing of intermediate data files is required during a normal run.

## 7. Key Outputs

The `data/` directory contains:

- `raw/movie_details.json` - retrieved movie details.
- `raw/movie_credits.json` - retrieved movie credits.
- `processed/movies.csv` - prepared movie records.
- `processed/credits.csv` - prepared credit records.
- `processed/analysis_movies.csv` - analysis-ready movie data.
- `processed/id_audit.csv` - input identifier audit.
- `quarantine/quarantined_records.csv` - records requiring exclusion or investigation.

The `outputs/` directory contains:

| File | Purpose |
|---|---|
| `candidate_metrics_all_years.csv` | All-years candidate metrics |
| `candidate_metrics_2000_onward.csv` | 2000-onward candidate metrics |
| `candidate_rankings_all_years.csv` | All-years candidate rankings |
| `candidate_rankings_2000_onward.csv` | 2000-onward candidate rankings |
| `comparison_summary.csv` | Franchise versus standalone comparison |
| `comparison_units_all_years.csv` | All-years comparison units |
| `comparison_units_2000_onward.csv` | 2000-onward comparison units |
| `shortlist_all_years.csv` | All-years shortlist |
| `shortlist_2000_onward.csv` | 2000-onward shortlist |
| `shortlist_stability.csv` | Candidates appearing across both periods |
| `talent_metrics_all_years.csv` | All-years candidate-level talent metrics |
| `talent_metrics_2000_onward.csv` | 2000-onward candidate-level talent metrics |
| `talent_person_metrics_all_years.csv` | All-years individual talent metrics |
| `talent_person_metrics_2000_onward.csv` | 2000-onward individual talent metrics |

## 8. Ranking Methodology

The final candidate ranking uses the following weights:

| Metric | Weight |
|---|---:|
| Historical revenue-to-budget ratio | 50% |
| Audience rating | 25% |
| TMDb popularity | 25% |
| Cast score | 0% |
| Director score | 0% |

Scores are percentile-based within each candidate category. Franchise and standalone scores should not be compared directly.

Talent indicators are analysed separately as supporting evidence rather than used as ranking drivers.

## 9. Data Quality and Limitations

The supplied dataset contained:

- 126 input rows.
- 112 successfully retrieved unique films.
- 5 valid identifiers that returned unavailable/not-found responses.
- 6 duplicate rows.
- 2 invalid identifiers.
- 1 missing identifier.

The retrieved films cover release years 1966 to 2019, with no post-2019 titles.

Other limitations include:

- TMDb financial figures were not independently verified.
- TMDb popularity is a platform measure, not historical audience demand.
- Revenue-to-budget ratio is not profit or licensing return on investment.
- Films without a TMDb collection are treated as standalone candidates for operational purposes.
- Franchise results reflect only the films represented in the supplied dataset.
- Licensing prices, rights availability, territory restrictions and StreamVault-specific audience demand were not provided.

See `data_findings.md` and `questions.md` for the detailed data diagnosis, decisions and outstanding questions.

## 10. Reproducibility and Scaling

The project uses a central configuration file, environment-based API authentication and an automated pipeline to support repeatable execution.

The input file can accommodate a larger list of TMDb identifiers without changing the analysis workflow.

However, the current analysis has been run against the supplied 126-row file. A full test using approximately 500 identifiers has **not yet been completed**. Actual runtime will depend on API response times, rate limits and retries.

For a fresh setup, Adjoa should be able to clone the repository, install the dependencies, configure her own API token and run `python main.py` to regenerate the analysis.

## 11. Decision Documentation

The `decision/` directory contains four Architecture Decision Records documenting important analytical choices, alternatives considered and trade-offs.

Additional business deliverables:

- `recommendation.md` - detailed recommendation and shortlists.
- `client_memo.md` - concise business-facing summary.
- `data_findings.md` - data diagnosis and ranked risks.
- `questions.md` - analytical questions, decisions and unresolved client information.

## 12. Additional Improvement

A shortlist stability analysis compares candidates appearing in both analysis windows. It identifies recommendations that remain consistent when the release-year scope changes and makes the decision process more transparent.

## 13. Troubleshooting

**TMDb authentication error (401)**

- Check that your `.env` file is in the project root.
- Confirm that the variable is named `TMDB_ACCESS_TOKEN`.
- Check that your token is valid.
- Do not share your token publicly.

**Unavailable movie identifiers (404)**

Some identifiers may not return movie details or credits. These are recorded in the audit and quarantine outputs. A 404 does not automatically mean the entire pipeline has failed.

**Missing Python module errors**

- Activate the virtual environment.
- Install dependencies using `python -m pip install -r requirements.txt`.
- Run the complete project from its root directory using `python main.py`.

**Network or API failures**

Check your internet connection and TMDb API access. Retry the pipeline when the service is available.

## 14. Disclaimer

Historical box-office performance and platform indicators are screening measures only. Final licensing decisions should be supported by rights verification, current market demand, commercial terms and an assessment of expected licensing economics.