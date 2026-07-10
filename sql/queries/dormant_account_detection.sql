WITH activity_days AS (
    SELECT DISTINCT account_id, DATE_TRUNC('day', transaction_timestamp)::date AS activity_date
    FROM fact_transactions
),
calendar AS (
    SELECT a.account_id, d::date AS calendar_date
    FROM dimension_account a
    CROSS JOIN generate_series(
        (SELECT MIN(activity_date) FROM activity_days),
        CURRENT_DATE,
        INTERVAL '1 day'
    ) AS d
),
activity_flagged AS (
    SELECT c.account_id, c.calendar_date,
           CASE WHEN ad.activity_date IS NULL THEN 0 ELSE 1 END AS is_active
    FROM calendar c
    LEFT JOIN activity_days ad ON c.account_id = ad.account_id AND c.calendar_date = ad.activity_date
),
islands AS (
    SELECT account_id, calendar_date, is_active,
        calendar_date - (ROW_NUMBER() OVER (
            PARTITION BY account_id, is_active ORDER BY calendar_date
        ))::int AS island_group
    FROM activity_flagged
)
SELECT account_id, MIN(calendar_date) AS dormant_from, MAX(calendar_date) AS dormant_to,
       COUNT(*) AS dormant_days
FROM islands
WHERE is_active = 0
GROUP BY account_id, island_group
HAVING COUNT(*) >= 30
ORDER BY dormant_days DESC
LIMIT 10;