WITH trans AS (
    SELECT
        Month(cashflow_date) AS tran_month
        , CASE WHEN Day(cashflow_date) < 15 THEN 'bot' else 'top' 
            END AS tran_period
        , accountid
        , categoryid
        , transaction_type
        , amount
    FROM transactions 
    WHERE accountid IN (
      SELECT accountid FROM account
      WHERE account_type IN ('Checking', 'Credit Card')
    )
        AND categoryid NOT IN (
            SELECT categoryid FROM category
            WHERE category_name = 'Card Payment'
        )
        AND cashflow_date >= Date_Add(ConCat(YEAR(Now()), '-', MONTH(Now()), '-', '01'), INTERVAL -6 MONTH )
), top_bot AS (
    SELECT
        tran_month, tran_period
        , sum(amount) AS amount
    FROM trans
    GROUP BY tran_month, tran_period
)
SELECT
    tran_month, 'total' AS tran_period
    , sum(amount) AS amount
FROM top_bot
GROUP BY tran_month
UNION
SELECT * FROM top_bot
ORDER BY tran_month, tran_period
;