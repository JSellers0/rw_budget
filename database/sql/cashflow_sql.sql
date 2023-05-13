WITH chk AS (
  SELECT
    Sum(DISTINCT Coalesce(ab.balance, 0)) AS chk_balance
    , Sum(CASE WHEN transaction_type = 'debit' AND Extract(DAY FROM transaction_date) < 15 
        THEN amount END) AS chk_in_top
    , Sum(CASE WHEN transaction_type = 'credit'  AND Extract(DAY FROM transaction_date) < 15 
        THEN amount END) AS chk_out_top
    , Sum(CASE WHEN transaction_type = 'debit' AND Extract(DAY FROM transaction_date) > 14 
        THEN amount END) AS chk_in_bot
    , Sum(CASE WHEN transaction_type = 'credit'  AND Extract(DAY FROM transaction_date) > 14 
        THEN amount END) AS chk_out_bot
  FROM transactions t
    LEFT JOIN accountbalance ab ON ab.accountid = t.accountid
      AND ab.agg_start = '2023-04-01'
  WHERE transaction_date BETWEEN '2023-05-01' AND '2023-05-30'
    AND t.accountid IN (
      SELECT accountid FROM account
      WHERE account_type = 'Checking'
    )
    AND t.categoryid NOT IN (
      SELECT categoryid FROM category
      WHERE category_name = 'Card Payment'
    )
), card AS (
  SELECT
    Sum(DISTINCT Coalesce(ab.balance, 0)) AS card_balance
    , Sum(CASE WHEN transaction_type = 'debit' AND Extract(DAY FROM transaction_date) < 15 
        THEN amount END) AS card_in_top
    , Sum(CASE WHEN transaction_type = 'credit'  AND Extract(DAY FROM transaction_date) < 15 
        THEN amount END) AS card_out_top
    , Sum(CASE WHEN transaction_type = 'debit' AND Extract(DAY FROM transaction_date) > 14 
        THEN amount END) AS card_in_bot
    , Sum(CASE WHEN transaction_type = 'credit'  AND Extract(DAY FROM transaction_date) > 14 
        THEN amount END) AS card_out_bot
  FROM transactions t
    LEFT JOIN accountbalance ab ON ab.accountid = t.accountid
      AND ab.agg_start = '2023-04-01'
  WHERE transaction_date BETWEEN '2023-05-01' AND '2023-05-30'
    AND t.accountid IN (
      SELECT accountid FROM account
      WHERE account_type = 'Credit Card'
    )
), summary AS (
  SELECT
    chk_balance + chk_in_top + chk_in_bot AS cash_in_sum
    , card_balance + chk_out_top + chk_out_bot + card_out_top + card_out_bot AS cash_out_sum
    , (chk_balance + chk_in_top + chk_in_bot) + (card_balance + chk_out_top + chk_out_bot + card_out_top + card_out_bot) AS cash_remain_sum
  FROM chk, card
), top AS (
  SELECT
    chk_balance + chk_in_top AS cash_in_top
    , card_balance + chk_out_top + card_out_top AS cash_out_top
    , chk_balance + chk_in_top + card_balance + chk_out_top + card_out_top AS cash_remain_top
    , card_balance + card_in_top + card_out_top AS card_top_balance
  FROM chk, card
), top_bot AS (
  SELECT
    top.*
    , cash_remain_top + chk.chk_in_bot AS cash_in_bot
    , top.card_top_balance + card.card_out_bot + chk.chk_out_bot AS cash_out_bot
    , (cash_remain_top + chk.chk_in_bot) + (top.card_top_balance + card.card_out_bot + chk.chk_out_bot) AS cash_remain_bot
  FROM top, chk, card
)
SELECT *
FROM summary, top_bot
;