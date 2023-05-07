CREATE OR REPLACE VIEW vw_card_current_balances
AS

SELECT t.transactionid
FROM transaction t
;

SELECT
    bal.accountid, a.account_name, bal.chg_bal, bal.pmt_bal
    , bal.cur_bal + IfNull(ab.balance, 0) AS cur_bal
    , bal.pnd_bal + IfNull(ab.balance, 0) AS pnd_bal
FROM (
    SELECT
        accountid
        , Sum(CASE 
            WHEN is_pending = 0 AND transaction_type = 'credit'
                THEN amount ELSE 0 END) AS chg_bal
        , Sum(CASE
            WHEN is_pending = 0 AND transaction_type = 'debit'
                THEN amount ELSE 0 END) AS pmt_bal
        , Sum(CASE
            WHEN is_pending = 0 THEN amount
            ELSE 0 END) AS cur_bal
        , Sum(amount) AS pnd_bal
    FROM transaction
    WHERE transaction_date BETWEEN '2023-05-01' AND '2023-05-14'
    GROUP BY accountid
) bal
    INNER JOIN account a ON a.accountid = bal.accountid
    LEFT JOIN accountbalance ab ON ab.accountid = bal.accountid
        AND ab.is_current = 1
WHERE a.account_type = 'Credit Card'