SELECT
        bal.accountid, a.account_name
        , IfNull(bal.chg_bal, 0) AS chg_bal, IfNull(bal.pmt_bal, 0) AS pmt_bal
        , IfNull(bal.cur_bal, 0) + IfNull(ab.balance, 0) AS cur_bal
        , IfNull(bal.pnd_bal, 0) + IfNull(ab.balance, 0) AS pnd_bal
    FROM account a
        LEFT JOIN (
        SELECT
            accountid
            , Sum(CASE 
                WHEN transaction_date <= CurDate() AND transaction_type = 'credit'
                    THEN amount ELSE 0 END) AS chg_bal
            , Sum(CASE
                WHEN transaction_date <= CurDate() AND transaction_type = 'debit'
                    THEN amount ELSE 0 END) AS pmt_bal
            , Sum(CASE
                WHEN transaction_date <= CurDate() THEN amount
                ELSE 0 END) AS cur_bal
            , Sum(amount) AS pnd_bal
        FROM transactions
        WHERE transaction_date BETWEEN '{start}' AND '{end}'
        GROUP BY accountid
    ) bal
        ON a.accountid = bal.accountid
        LEFT JOIN accountbalance ab ON ab.accountid = bal.accountid
            AND ab.agg_start = Date_Add('{start}', INTERVAL -1 MONTH)
    WHERE a.account_type = 'Credit Card'
    ;