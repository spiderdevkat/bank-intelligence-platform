# Bank Intelligence Platform — Checkpoint Roadmap

## Phase 0 — Environment Setup
- [x] 0.1 Verify Python/Git/Docker tools
- [x] 0.2 Create project folder
- [x] 0.3 .gitignore + first commit
- [x] 0.4 Virtual environment
- [x] 0.5 Verify local Postgres + MongoDB, connect to both
- [x] 0.6 Install core Python dependencies

## Phase 1 — Python + Synthetic Data Generation
- [x] 1.0 Install faker
- [x] 1.1 Data models (dataclasses, enums)
- [x] 1.2 Customer generator
- [x] 1.3 Account generator (hierarchies)
- [x] 1.4 Normal transaction generator
- [x] 1.5 Fraud pattern injectors (velocity, structuring, round-tripping)
- [x] 1.6 CLI entry script
- [x] 1.7 Unit tests
- [x] 1.8 Concurrency mini-lab (threading/multiprocessing/asyncio + GIL)

## Phase 2 — Web Scraping + MongoDB
- [ ] 2.1 Connect to MongoDB with pymongo
- [ ] 2.2 SEC EDGAR scraper
- [ ] 2.3 Finnhub API client (news)
- [ ] 2.4 FRED API client (macro data)
- [ ] 2.5 Frankfurter API client (FX rates)
- [ ] 2.6 Land raw data into MongoDB

## Phase 3 — SQL Data Modeling
- [ ] 3.1 Connect Python to Postgres
- [ ] 3.2 Star schema design
- [ ] 3.3 SCD Type 2 customer dimension
- [ ] 3.4 Load data into Postgres
- [ ] 3.5 Core SQL (SELECT/JOIN/GROUP BY)
- [ ] 3.6 Window functions
- [ ] 3.7 Recursive CTE
- [ ] 3.8 Gaps-and-islands query
- [ ] 3.9 Query tuning (EXPLAIN ANALYZE + indexes)

## Phase 4 — Spark SQL
- [ ] 4.1 PySpark local session
- [ ] 4.2 Load Postgres data into Spark
- [ ] 4.3 Rewrite SQL as Spark SQL
- [ ] 4.4 Skew simulation + salting/broadcast
- [ ] 4.5 Gold layer job

## Phase 5 — Statistics + Classical ML
- [ ] 5.1 Hypothesis testing (t-test)
- [ ] 5.2 Chi-square test
- [ ] 5.3 Feature engineering
- [ ] 5.4 Regression
- [ ] 5.5 KNN
- [ ] 5.6 KMeans clustering
- [ ] 5.7 Random Forest fraud classifier

## Phase 6 — GenAI
- [ ] 6.1 Gemini API + prompt engineering
- [ ] 6.2 Text-to-SQL with guardrails
- [ ] 6.3 LLM summary generator

## Phase 7 — RAG + LangChain + Agentic AI
- [ ] 7.1 Embeddings + vector store
- [ ] 7.2 RAG pipeline
- [ ] 7.3 LangChain rebuild
- [ ] 7.4 Fraud Investigator Agent

## Phase 8 — Tableau (final step)
- [ ] 8.1 Connect Tableau to Postgres
- [ ] 8.2 Build dashboards

## Phase 9 — Wrap-up
- [ ] 9.1 Final docs/tests cleanup