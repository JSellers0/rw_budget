CREATE OR REPLACE PROCEDURE sp_agg_account_balances()
BEGIN
    DECLARE ed DATE;
    DECLARE sd DATE;

    SET ed = Date_Add(CURDATE(), INTERVAL -1 DAY);
    IF Extract(DAY FROM CURDATE()) = 1 THEN
        SET sd = ConCat(Extract(YEAR FROM @ed), '-', Extract(MONTH FROM @ed), '-15');
    ELSEIF Extract(DAY FROM CURDATE()) = 15 THEN
        SET sd = Date_Add(CURDATE(), INTERVAL -14 DAY);
    END IF;

    CREATE OR REPLACE TEMPORARY TABLE agg_bal (
        accountid INTEGER, balance DECIMAL(7,2)
    );

    INSERT INTO agg_bal (accountid, balance)
    SELECT accountid,  sum(balance) as balance
    FROM (
        SELECT
            t.accountid, sum(t.amount) AS balance
        FROM transaction t
        WHERE t.transaction_date BETWEEN @sd AND @ed
        GROUP BY t.accountid
        UNION
        SELECT
            ab.accountid, ab.balance
        FROM accountbalance ab
        WHERE ab.is_current = 1
    ) bal_data
    GROUP BY accountid;

    UPDATE accountbalance
    SET is_current = 0;

    INSERT INTO accountbalance (accountid, balance, is_current, agg_period)
    SELECT
        accountid, balance, 1, ConCat(@sd, '-', @ed)
    FROM agg_bal
    ;

    DROP TABLE agg_bal
    ;
END;