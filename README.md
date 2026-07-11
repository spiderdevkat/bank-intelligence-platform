# Bank Intelligence Platform

An end-to-end, hands-on learning project simulating a bank's data and risk
analytics platform — built from absolute zero, one file and one command
at a time, across 9 phases: synthetic data generation, web scraping,
SQL data modeling, Spark SQL, statistics/ML, GenAI, RAG, LangChain,
agentic AI, and Tableau visualization.

**Live dashboard:** https://public.tableau.com/views/Book1_17837674125150/BankFraudAnalyticsDashboard

## What this project actually does

Simulates a bank's transaction pipeline end-to-end:
1. Generates synthetic customers/accounts/transactions with **three
   structurally real fraud patterns** (velocity, structuring,
   round-tripping) — not just random labels
2. Scrapes real external data (SEC EDGAR filings, Finnhub news, FRED
   interest rates, Frankfurter FX rates) into MongoDB
3. Models everything into a proper star schema in Postgres, including a
   Slowly Changing Dimension (Type 2) for historical customer risk tiers
4. Reprocesses the data at "big data" scale with Spark SQL — including
   deliberately engineering data skew and fixing it with salting, and
   comparing sort-merge vs. broadcast joins
5. Runs real statistics (hypothesis testing, chi-square) and trains three
   ML models (Logistic Regression, KNN, Random Forest) to detect fraud,
   plus KMeans clustering for customer risk segmentation
6. Builds a GenAI layer: schema-aware text-to-SQL with a genuinely tested
   safety guardrail, RAG over scraped news, and a multi-tool
   **Fraud Investigator Agent** that combines SQL + ML + RAG to produce
   real investigation reports
7. Visualizes it all in an interactive Tableau Public dashboard

## Tech stack
Python 3.9, PostgreSQL 18, MongoDB 7, PySpark (via Google Colab),
scikit-learn, Google Gemini API, LangChain, Tableau Public

## Project structure

```text
bank-intelligence-platform/
├── data_generation/     # Phase 1: models, generators, fraud patterns
├── scraper/             # Phase 2: EDGAR, Finnhub, FRED, Frankfurter → MongoDB
├── sql/                 # Phase 3: star schema (SCD2), queries, tuning notes
├── spark_jobs/          # Phase 4: notes + gold layer (run via Colab)
├── ml/                  # Phase 5: stats tests, feature engineering, models
├── genai/               # Phase 6–7: Gemini client, text-to-SQL, RAG, agent
├── db/                  # PostgreSQL connection + loaders
├── tests/               # pytest suite
├── scripts/             # CLI entry points (generate_data.py, run_scraper.py, etc.)
├── ROADMAP.md           # Full checkpoint history
└── data/                # Generated CSVs (gitignored)
```

## Running it yourself

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Generate synthetic data
python scripts\generate_data.py --customers 500 --normal-txns 5000

# Scrape external data into MongoDB
python scripts\run_scraper.py

# Load into Postgres (see sql/ for schema)
# ... (apply sql/*.sql files, then use db/loader.py)

# Run the fraud investigator agent
python
>>> from genai.agent import investigate
>>> print(investigate("Investigate account <id> for potential fraud"))
```

See `ROADMAP.md` for the full checkpoint-by-checkpoint build history,
including real bugs hit and fixed along the way (not just a polished
final state).