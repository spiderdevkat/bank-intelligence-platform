WITH RECURSIVE account_tree AS (
    SELECT account_id, parent_account_id, account_number, 1 AS depth, ARRAY[account_id]::VARCHAR[] AS path
    FROM dimension_account
    WHERE parent_account_id IS NULL

    UNION ALL

    SELECT a.account_id, a.parent_account_id, a.account_number, t.depth + 1, t.path || a.account_id
    FROM dimension_account a
    JOIN account_tree t ON a.parent_account_id = t.account_id
)
SELECT account_number, depth, path
FROM account_tree
WHERE depth = 4;