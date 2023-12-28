CREATE OR REPLACE VIEW vw_cashflow_chart
AS
    WITH trans AS (
        SELECT
            Year(cashflow_date) AS tran_year
            , Month(cashflow_date) AS tran_month
            , MonthName(cashflow_date) AS tran_month_name
            , ConCat(Year(cashflow_date), '-', Month(cashflow_date), '-01') AS date_check
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
    ), top_bot AS (
        SELECT
            tran_year, tran_month, tran_month_name, date_check, tran_period
            , sum(amount) AS amount
        FROM trans
        GROUP BY  tran_year, tran_month, tran_month_name, date_check, tran_period
    )
    SELECT
         tran_year, tran_month, tran_month_name, date_check, 'total' AS tran_period
        , sum(amount) AS amount
    FROM top_bot
    GROUP BY  tran_year, tran_month, tran_month_name, date_check
    UNION
    SELECT * FROM top_bot
    ORDER BY  tran_year, tran_month, tran_period
;