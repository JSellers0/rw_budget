CREATE EVENT ev_agg_account_balances_01
    ON SCHEDULE EVERY 1 MONTH
    STARTS '2023-06-01 00:00:00'
DO CALL sp_agg_account_balances
;