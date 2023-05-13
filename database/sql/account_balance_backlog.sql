

INSERT INTO accountbalance (accountid, balance, agg_start, agg_end)
VALUES (5, -251.53, '2023-04-01', '2023-04-30')
;

SELECT *
FROM accountbalance
WHERE accountid = 1
;

UPDATE accountbalance
SET balance = 0
WHERE accountid = 1
AND agg_start = '2023-04-01'
;


SELECT
        a.accountid, a.account_name
        , IfNull(bal.chg_bal, 0) AS chg_bal, IfNull(bal.pmt_bal, 0) AS pmt_bal
        , IfNull(bal.cur_bal, 0) + IfNull(ab.balance, 0) AS cur_bal
        , IfNull(bal.pnd_bal, 0) + IfNull(ab.balance, 0) AS pnd_bal
    FROM account a
        LEFT JOIN (
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
            WHERE transaction_date BETWEEN '2023-03-01' AND '2023-03-14'
            GROUP BY accountid
        ) bal
            ON a.accountid = bal.accountid
        LEFT JOIN accountbalance ab ON ab.accountid = bal.accountid
            AND ab.agg_start = Date_Add('2023-03-01', INTERVAL -1 MONTH)
    WHERE a.account_type = 'Credit Card'
    ;

SELECT
    bal_data.accountid, sum(balance), '2023-04-01', '2023-04-30'
FROM (
    SELECT
        t.accountid, sum(t.amount) AS balance
    FROM transaction t
    WHERE t.transaction_date BETWEEN '2023-04-01' AND '2023-04-30'
    GROUP BY t.accountid
    UNION
    SELECT
        ab.accountid, ab.balance
    FROM accountbalance ab
    WHERE ab.agg_start = Date_Add('2023-04-01', INTERVAL -1 MONTH)
        AND ab.agg_end = Date_Add('2023-04-01', INTERVAL -1 DAY)
) bal_data
WHERE bal_data.accountid = 1
GROUP BY bal_data.accountid
;

DELETE FROM accountbalance
WHERE accountid = 1 AND agg_start = '2023-03-01'
;

INSERT INTO accountbalance (accountid, balance, agg_start, agg_end)
VALUES (1, -540.15, '2023-03-01', '2023-03-31')
;

--INSERT INTO accountbalance (accountid, balance, agg_start, agg_end)
;

SELECT
    bal_data.accountid, sum(balance), '2023-03-01', '2023-03-31'
FROM (
    SELECT
        t.accountid, sum(t.amount) AS balance
    FROM transaction t
    WHERE t.transaction_date BETWEEN '2023-03-01' AND '2023-03-31'
    GROUP BY t.accountid
    UNION
    SELECT
        ab.accountid, ab.balance
    FROM accountbalance ab
    WHERE ab.agg_start = Date_Add('2023-03-01', INTERVAL -1 MONTH)
        AND ab.agg_end = Date_Add('2023-03-01', INTERVAL -1 DAY)
) bal_data
WHERE bal_data.accountid = 1
GROUP BY bal_data.accountid
;

SELECT
        bal.accountid, a.account_name
        , IfNull(bal.chg_bal, 0) AS chg_bal, IfNull(bal.pmt_bal, 0) AS pmt_bal
        , bal.cur_bal AS bal_no_prior
        , ab.balance AS prior_bal
        , IfNull(bal.cur_bal, 0) + IfNull(ab.balance, 0) AS cur_bal
        , IfNull(bal.pnd_bal, 0) + IfNull(ab.balance, 0) AS pnd_bal
    FROM account a
        LEFT JOIN (
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
        WHERE transaction_date BETWEEN '2023-05-01' AND '2023-05-31'
        GROUP BY accountid
    ) bal
        ON a.accountid = bal.accountid
        LEFT JOIN accountbalance ab ON ab.accountid = bal.accountid
            AND ab.agg_start = Date_Add('2023-05-01', INTERVAL -1 MONTH)
    WHERE a.account_type = 'Credit Card'
;