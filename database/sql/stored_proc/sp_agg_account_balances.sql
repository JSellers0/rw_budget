CREATE OR REPLACE PROCEDURE sp_agg_account_balances()
this_proc:BEGIN
    
    DECLARE sd DATE;
    DECLARE ed DATE;

    IF Extract(DAY FROM CURDATE()) = 1 THEN
        SET sd = Date_Add(CURDATE(), INTERVAL -1 MONTH);
        SET ed = Date_Add(CURDATE(), INTERVAL -1 DAY);
    ELSE
        LEAVE this_proc;
    END IF;

    INSERT INTO accountbalance (accountid, balance, agg_start, agg_end)
    SELECT
        accountid, sum(balance), sd, ed
    FROM (
        SELECT
            t.accountid, sum(t.amount) AS balance
        FROM transaction t
        WHERE t.transaction_date BETWEEN sd AND ed
        GROUP BY t.accountid
        UNION
        SELECT
            ab.accountid, ab.balance
        FROM accountbalance ab
        WHERE ab.agg_start = Date_Add(sd, INTERVAL -1 MONTH)
    ) bal_data
    GROUP BY accountid
    ;
END;