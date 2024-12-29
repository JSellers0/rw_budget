CREATE OR REPLACE VIEW vw_cashflow AS
WITH chk AS (
  SELECT
  	Extract(MONTH FROM cashflow_date) AS flow_month
  	, Extract(YEAR FROM cashflow_date) AS flow_year
    , Sum(CASE WHEN transaction_type = 'debit' AND Extract(DAY FROM cashflow_date) < 15
          THEN amount ELSE 0 END) AS chk_in_top
    , Sum(CASE WHEN transaction_type = 'credit'  AND Extract(DAY FROM cashflow_date) < 15
          THEN amount ELSE 0 END) AS chk_out_top
    , Sum(CASE WHEN transaction_type = 'debit' AND Extract(DAY FROM cashflow_date) > 14
          THEN amount ELSE 0 END) AS chk_in_bot
    , Sum(CASE WHEN transaction_type = 'credit'  AND Extract(DAY FROM cashflow_date) > 14
          THEN amount ELSE 0 END) AS chk_out_bot
  FROM transactions t
  WHERE t.accountid IN (
      SELECT accountid FROM account
      WHERE account_type = 'Checking'
      )
      AND t.categoryid NOT IN (
      SELECT categoryid FROM category
      WHERE category_name = 'Card Payment'
      )
   GROUP BY Extract(MONTH FROM cashflow_date), Extract(YEAR FROM cashflow_date)
  ), card AS (
  SELECT
    Extract(MONTH FROM cashflow_date) AS flow_month
  	, Extract(YEAR FROM cashflow_date) AS flow_year
    , Sum(CASE WHEN transaction_type = 'debit' AND Extract(DAY FROM cashflow_date) < 15
          THEN amount ELSE 0 END) AS card_in_top
    , Sum(CASE WHEN transaction_type = 'credit'  AND Extract(DAY FROM cashflow_date) < 15
          THEN amount ELSE 0 END) AS card_out_top
    , Sum(CASE WHEN transaction_type = 'debit' AND Extract(DAY FROM cashflow_date) > 14
          THEN amount ELSE 0 END) AS card_in_bot
    , Sum(CASE WHEN transaction_type = 'credit'  AND Extract(DAY FROM cashflow_date) > 14
          THEN amount ELSE 0 END) AS card_out_bot
  FROM transactions t
  WHERE t.accountid IN (
      SELECT accountid FROM account
      WHERE account_type = 'Credit Card'
      )
      AND t.categoryid NOT IN (
      SELECT categoryid FROM category
      WHERE category_name IN ('Card Payment', 'Finance Payment')
      )
  GROUP BY Extract(MONTH FROM cashflow_date), Extract(YEAR FROM cashflow_date)
  ), summary AS (
  SELECT
    	chk.flow_year, chk.flow_month
      # Summary
      , (chk_in_top + chk_in_bot + IfNull(card_in_top, 0) + IfNull(card_in_bot, 0)) +
        (chk_out_top + chk_out_bot + IfNull(card_out_top, 0) + IfNull(card_out_bot, 0)) AS cash_remain_sum
      , chk_in_top + chk_in_bot AS cash_in_sum
      , chk_out_top + chk_out_bot + IfNull(card_out_top, 0) + IfNull(card_out_bot, 0) AS cash_out_sum
      # Top
      , chk_in_top + IfNull(card_in_top, 0) + chk_out_top + IfNull(card_out_top, 0) AS cash_remain_top
      , chk_in_top + IfNull(card_in_top, 0) AS cash_in_top
      , chk_out_top + IfNull(card_out_top, 0) AS cash_out_top
      # Bot
      , chk_in_bot + IfNull(card_in_bot, 0) + chk_out_bot + IfNull(card_out_bot, 0) AS cash_remain_bot
      , chk_in_bot + IfNull(card_in_bot, 0) AS cash_in_bot
      , chk_out_bot + IfNull(card_out_bot, 0) AS cash_out_bot
  FROM chk
    LEFT JOIN card
    	ON card.flow_month = chk.flow_month
    	AND card.flow_year = chk.flow_year
  )
  SELECT *
  FROM summary
  ;