# Spark SQL — Phase 4 Notes

All Phase 4 work was done in Google Colab (PySpark on Windows has painful
Java/winutils setup, not worth fighting for a learning project). Postgres
tables were exported to CSV and loaded into Spark DataFrames there.

## What was covered
- Schema inference gotcha: Postgres boolean `t`/`f` doesn't map to Spark
  boolean automatically — required an explicit `when/otherwise` cast.
- Rewrote the Phase 3 velocity fraud CTE as Spark SQL — same result (69
  velocity, 17 structuring, 9 round-tripping), confirming SQL syntax
  transfers directly between engines with minor dialect differences
  (e.g. `INTERVAL 15 MINUTES` vs Postgres's `INTERVAL '15 minutes'`).
- Read `.explain(True)` output: parsed -> analyzed -> optimized -> physical
  plan. Saw Catalyst's column pruning in action (unused columns dropped
  before the optimized plan).
- Data skew: built a synthetic "whale customer" dataset (40k rows vs
  ~300 for everyone else). Had to disable AQE's coalescePartitions to
  actually see the skew (it was auto-hiding the problem). Measured a
  40,000-row max partition, fixed with salting down to ~4,800 max,
  verified the salt-then-recombine round trip preserved the correct
  total count (40,000).
- Broadcast joins: compared SortMergeJoin (both sides shuffled) vs
  BroadcastHashJoin (only the small table copied, large table never
  shuffled) using dimension_account (313 rows) against fact_transactions.

## Gold layer
Built `gold_daily_account_summary`: a daily, per-account aggregation
(transaction_count, total_volume, avg_transaction_amount, fraud_count)
collapsing 2,095 raw transactions into 1,987 summary rows. Written as
parquet (columnar format — only needed columns get read off disk,
unlike CSV which always reads every column). Output saved to
spark_jobs/output/.