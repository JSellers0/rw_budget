"""
# ToDo: Get all transactions by accountid
# DECISION: Return all account transactions and let web layer filter by dates?  Or get by account and date function?
# ToDo: Standardize response messages
# ToDo: Response status checks where appropriate
# ToDo: try/except around db operations?
# ToDo: use get functions instead of repeating Transaction.query in insert,update,delete
# ToDo: Recurring transaction CRUD
# ToDo: ispending flag to all get methods
# ToDo: set ispending flag on insert/update
"""
# IMPORTS
from app import db
from controllers.objects.models import Transaction, TransactionInterface, RecurringTransaction
from dataclasses import dataclass
from datetime import date, timedelta
import pandas as pd
from sqlalchemy import text


# CONSTANTS
CASHFLOW_CHART_SEGMENTS = 3

@dataclass
class TransactionResponse():
    response_code: int
    message: str
    transactions: list[TransactionInterface]


def get_all_transactions() -> TransactionResponse:
    transactions = Transaction.query.order_by(
        Transaction.transaction_date.desc()).all()

    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message="No transactions found",
            transactions=[None]  # type: ignore
        )

    return TransactionResponse(
        response_code=200,
        message=f"Retrieved {len(transactions)} transactions.",
        transactions=[TransactionInterface(
            transaction, transaction.category, transaction.account) for transaction in transactions]
    )


def get_transaction_by_id(transactionid: int) -> TransactionResponse:
    transaction = Transaction.query.filter(
        Transaction.transactionid == transactionid).one_or_none()

    if transaction is None:
        return TransactionResponse(
            response_code=404,
            message="No transactions found",
            transactions=[None]  # type: ignore
        )

    return TransactionResponse(
        response_code=200,
        message=f"Successfully retrieved transaction {transactionid}.",
        transactions=[TransactionInterface(
            transaction, transaction.category, transaction.account)]
    )


def get_transactions_by_date(date: str) -> TransactionResponse:
    transactions = Transaction.query.filter(
        Transaction.transaction_date == date).all()

    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message=f"No transactions found on {date}",
            transactions=[None]  # type: ignore
        )

    return TransactionResponse(
        response_code=200,
        message=f"Retrieved {len(transactions)} on {date}.",
        transactions=[TransactionInterface(
            transaction, transaction.category, transaction.account) for transaction in transactions]
    )


def get_transactions_by_date_range(start: str, end: str = '') -> TransactionResponse:
    transactions = []
    if end:
        transactions = Transaction.query.filter(Transaction.transaction_date <= end).filter(
            Transaction.transaction_date >= start).order_by(Transaction.transaction_date.desc()).all()
    else:
        transactions = Transaction.query.filter(Transaction.transaction_date >= start).order_by(
            Transaction.transaction_date.desc()).all()
    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message=f"No transactions found between {start} and {end}",
            transactions=[None]  # type: ignore
        )

    return TransactionResponse(
        response_code=200,
        message=f"Retrieved {len(transactions)} between {start} and {end}.",
        transactions=[TransactionInterface(
            transaction, transaction.category, transaction.account) for transaction in transactions]
    )


def get_transactions_by_category(categoryid: int) -> TransactionResponse:
    transactions = Transaction.query.filter(
        Transaction.categoryid == categoryid).all()
    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message=f"No transactions found for category {categoryid}",
            transactions=[None]  # type: ignore
        )

    return TransactionResponse(
        response_code=200,
        message=f"Retrieved {len(transactions)} for category {categoryid}.",
        transactions=[TransactionInterface(
            transaction, transaction.category, transaction.account) for transaction in transactions]
    )


def get_twenty_recent_transactions() -> TransactionResponse:
    transactions = Transaction.query.order_by(
        Transaction.transaction_date.desc()).limit(20)
    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message="No transactions found.",
            transactions=[None]  # type: ignore
        )

    return TransactionResponse(
        response_code=200,
        message=f"Retrieved {len(transactions)}.",
        transactions=[TransactionInterface(
            transaction, transaction.category, transaction.account) for transaction in transactions]
    )


def insert_transaction(transaction_data: dict) -> TransactionResponse:
    # Make sure credit values are negative
    if transaction_data.get('transaction_type', '') in ('credit', 'fin'):
        if transaction_data.get('amount', 0) > 0:
            transaction_data['amount'] = transaction_data['amount'] * -1

    # ToDo: Check for record with the exact same values?

    transaction: Transaction = Transaction(
        transaction_date=transaction_data.get(
            'transaction_date', date.today()),
        cashflow_date=transaction_data.get('cashflow_date', date.today()),
        merchant_name=transaction_data.get('merchant_name', ''),
        categoryid=transaction_data.get('category', 1),
        amount=transaction_data.get('amount', 0),
        accountid=transaction_data.get('account', 1),
        transaction_type=transaction_data.get('transaction_type', ''),
        note=transaction_data.get('note', '')
    )

    db.session.add(transaction)
    db.session.commit()

    return TransactionResponse(
        response_code=200,
        message="Transaction insert successful.",
        transactions=[TransactionInterface(
            transaction, transaction.category, transaction.account)]
    )


def update_transaction(transaction_data: dict) -> TransactionResponse:
    transaction: Transaction = Transaction.query.filter(
        Transaction.transactionid == transaction_data.get('transactionid')).one_or_none()

    if transaction is None:
        return TransactionResponse(
            response_code=404,
            message=f"Transaction { transaction_data.get('transactionid')} not found.",
            transactions=[None]  # type: ignore
        )

    # Make sure credit values are negative
    if transaction_data.get('transaction_type', '') in ('credit', 'fin'):
        if transaction_data.get('amount', 0) > 0:
            transaction_data['amount'] = transaction_data['amount'] * -1

    if transaction_data.get('transaction_date') != transaction.transaction_date:
        transaction.transaction_date = transaction_data.get(
            'transaction_date', '')  # type: ignore
    if transaction_data.get('cashflow_date') != transaction.cashflow_date:
        transaction.cashflow_date = transaction_data.get(
            'cashflow_date', '')  # type: ignore
    if transaction_data.get('merchant_name') != transaction.merchant_name:
        transaction.merchant_name = transaction_data.get(
            'merchant_name', '')  # type: ignore
    if transaction_data.get('category') != transaction.categoryid:
        transaction.categoryid = transaction_data.get(
            'category', 1)  # type: ignore
    if transaction_data.get('amount') != transaction.amount:
        transaction.amount = transaction_data.get('amount', 0)  # type: ignore
    if transaction_data.get('account') != transaction.accountid:
        transaction.accountid = transaction_data.get(
            'account', 0)  # type: ignore
    if transaction_data.get('transaction_type') != transaction.transaction_type:
        transaction.transaction_type = transaction_data.get(
            'transaction_type', '')  # type: ignore
    if transaction_data.get('note') != transaction.note:
        transaction.note = transaction_data.get('note', '')  # type: ignore

    db.session.commit()

    return TransactionResponse(
        response_code=200,
        message="Transaction update successful.",
        transactions=[TransactionInterface(
            transaction, transaction.category, transaction.account)]
    )


def delete_transaction(transactionid: int) -> TransactionResponse:
    transaction = Transaction.query.filter(
        Transaction.transactionid == transactionid).one_or_none()

    if transaction is None:
        raise ValueError(f"{transactionid} is not a valid transaction id.")

    transactions = [TransactionInterface(
        transaction, transaction.category, transaction.account)]

    db.session.delete(transaction)
    db.session.commit()

    return TransactionResponse(
        response_code=200,
        message=f"Transaction {transactionid} deleted successfully.",
        transactions=transactions
    )


def upload_transactions(filename: str) -> TransactionResponse:
    return TransactionResponse(
        response_code=200,
        message="count Transactions uploaded successfully.",
        transactions=[]
    )


def get_all_recurring_transactions() -> TransactionResponse:
    r_trans = RecurringTransaction.query.order_by(
        RecurringTransaction.expected_day.asc()).all()
    return TransactionResponse(
        response_code=200,
        message=f"Retrieved {len(r_trans)} recurring transactions.",
        transactions=[TransactionInterface(
            r_tran, r_tran.category, r_tran.account) for r_tran in r_trans]
    )


def get_rtran_by_id(rtranid: int) -> TransactionResponse:
    r_tran = RecurringTransaction.query.filter(
        RecurringTransaction.rtranid == rtranid).one_or_none()

    if r_tran is None:
        return TransactionResponse(
            response_code=404,
            message="No transactions found",
            transactions=[None]  # type: ignore
        )

    return TransactionResponse(
        response_code=200,
        message=f"Successfully retrieved transaction {rtranid}.",
        transactions=[TransactionInterface(
            r_tran, r_tran.category, r_tran.account)]
    )


def insert_recurring_transaction(transaction_data: dict) -> TransactionResponse:
    # Make sure credit values are negative
    if transaction_data.get('transaction_type', '') == 'credit':
        if transaction_data.get('amount', 0) > 0:
            transaction_data['amount'] = transaction_data['amount'] * -1

    # ToDo: Check for record with the exact same values?

    transaction: RecurringTransaction = RecurringTransaction(
        expected_day=transaction_data.get('expected_day'),
        merchant_name=transaction_data.get('merchant_name', ''),
        categoryid=transaction_data.get('category', 1),
        amount=transaction_data.get('amount', 0),
        accountid=transaction_data.get('account', 1),
        transaction_type=transaction_data.get('transaction_type'),
        is_monthly=transaction_data.get('is_monthly', True),
        note=transaction_data.get('note', ''),
    )

    db.session.add(transaction)
    db.session.commit()

    return TransactionResponse(
        response_code=200,
        message="Transaction insert successful.",
        transactions=[TransactionInterface(
            transaction, transaction.category, transaction.account)]
    )


def update_recurring_transaction(transaction_data: dict) -> TransactionResponse:
    transaction: RecurringTransaction = RecurringTransaction.query.filter(
        RecurringTransaction.rtranid == transaction_data.get('rtranid')).one_or_none()

    if transaction is None:
        return TransactionResponse(
            response_code=404,
            message=f"Transaction { transaction_data.get('rtranid')} not found.",
            transactions=[None]  # type: ignore
        )

    # Make sure credit values are negative
    if transaction_data.get('transaction_type', '') == 'credit':
        if transaction_data.get('amount', 0) > 0:
            transaction_data['amount'] = transaction_data['amount'] * -1

    if transaction_data.get('expected_day') != transaction.expected_day:
        transaction.expected_day = transaction_data.get(
            'expected_day', '')  # type: ignore
    if transaction_data.get('merchant_name') != transaction.merchant_name:
        transaction.merchant_name = transaction_data.get(
            'merchant_name', '')  # type: ignore
    if transaction_data.get('category') != transaction.categoryid:
        transaction.categoryid = transaction_data.get(
            'category', 1)  # type: ignore
    if transaction_data.get('amount') != transaction.amount:
        transaction.amount = transaction_data.get('amount', 0)  # type: ignore
    if transaction_data.get('account') != transaction.accountid:
        transaction.accountid = transaction_data.get(
            'account', 0)  # type: ignore
    if transaction_data.get('transaction_type') != transaction.transaction_type:
        transaction.transaction_type = transaction_data.get(
            'transaction_type', '')  # type: ignore
    if transaction_data.get('is_monthly') != transaction.is_monthly:
        transaction.is_monthly = transaction_data.get(
            'is_monthly', True)  # type: ignore
    if transaction_data.get('note') != transaction.note:
        transaction.note = transaction_data.get('note', '')  # type: ignore

    db.session.commit()

    return TransactionResponse(
        response_code=200,
        message="Transaction update successful.",
        transactions=[TransactionInterface(
            transaction, transaction.category, transaction.account)]
    )


def delete_recurring_transaction(rtranid: int) -> TransactionResponse:
    transaction: RecurringTransaction = RecurringTransaction.query.filter(
        RecurringTransaction.rtranid == rtranid).one_or_none()

    if transaction is None:
        raise ValueError(f"{rtranid} is not a valid transaction id.")

    transactions = [TransactionInterface(
        transaction, transaction.category, transaction.account)]

    db.session.delete(transaction)
    db.session.commit()

    return TransactionResponse(
        response_code=200,
        message=f"Transaction {rtranid} deleted successfully.",
        transactions=transactions
    )


def apply_recurring_transactions(rtrans_data: dict[str, str]) -> TransactionResponse:
    transactions = []
    for rtranid in rtrans_data.get("RTranIDs", "").split(","):
        # ToDo: Check Response
        get_rtran_response = get_rtran_by_id(int(rtranid))
        rtran = get_rtran_response.transactions[0]

        rtran_year = rtrans_data.get('rtran_year')
        rtran_month = rtrans_data.get('rtran_month')

        if rtran_year is None or rtran_month is None:
            return TransactionResponse(
                response_code=400,
                message="Bad Request: Please submit a year and month for correct processing.",
                transactions=[]
            )

        tran_data = {
            # type: ignore
            "transaction_date": date(year=int(rtran_year), month=int(rtran_month), day=rtran.transaction.expected_day),
            # type: ignore
            "cashflow_date": date(year=int(rtran_year), month=int(rtran_month), day=rtran.transaction.expected_day),
            "merchant_name": rtran.transaction.merchant_name,  # type: ignore
            "category": rtran.transaction.categoryid,  # type: ignore
            "amount": rtran.transaction.amount,  # type: ignore
            "account": rtran.transaction.accountid,  # type: ignore
            "transaction_type": rtran.transaction.transaction_type,  # type: ignore
            "note": rtran.transaction.note,  # type: ignore
        }
        # ToDo: Check Response
        tran_insert_response = insert_transaction(transaction_data=tran_data)
        transactions.append(tran_insert_response.transactions[0])

    return TransactionResponse(
        response_code=200,
        message=f"Successfully inserted {len(transactions)} recurring transactions.",
        transactions=transactions
    )


def get_month_end(year: int, month: int) -> date:
    if month == 12:
        next_month = 1
        year = year + 1
    else:
        next_month = month + 1
        year = year
    return date(year, next_month, 1) - timedelta(days=1)


def get_cashflow_df(flow_month: str, flow_year: str) -> dict:
    cashflow_sql = "SELECT cashflow_grp, amount\n"
    cashflow_sql += "FROM vw_cashflow_summary\n"
    cashflow_sql += f"WHERE flow_month = {flow_month}\n"
    cashflow_sql += f"\tAND flow_year = {flow_year}"

    results = db.session.execute(text(cashflow_sql))

    cashflow_data = {}
    for data in results:
        if data[0] is None:
            return {
                "sum": {
                    "remain": '$0.00',
                    "income": '$0.00',
                    "expens": '$0.00',
                },
                "top": {
                    "remain": '$0.00',
                    "income": '$0.00',
                    "expens": '$0.00',
                },
                "bot": {
                    "remain": '$0.00',
                    "income": '$0.00',
                    "expens": '$0.00',
                }
            }
        cashflow_grp = data[0].split('_')
        cashflow_data[cashflow_grp[1]][cashflow_grp[0]] = data[1]

    return cashflow_data


def get_credit_card_data(start: str, end: str) -> pd.DataFrame:
    # Direct SQL for now.  Need to learn stored procedures in MariaDB
    # or at least put this in a file instead of in the code.

    card_data_sql = f"""
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
        LEFT JOIN accountbalance ab ON ab.accountid = a.accountid
            AND ab.agg_start = Date_Add('{start}', INTERVAL -1 MONTH)
    WHERE a.account_type = 'Credit Card'
    ;
    """

    results = db.session.execute(text(card_data_sql))

    card_data = []
    for card in results:
        card_data.append(
            {
                "accountid": card[0],
                "account_name": card[1],
                "chg_bal": card[2],
                "pmt_bal": card[3],
                "cur_bal": card[4],
                "pnd_bal": card[5],
            }
        )

    card_data_df = pd.DataFrame.from_records(
        card_data,
        index='accountid',
        columns=card_data[0].keys()
    )

    return card_data_df


def get_cashflow(year: int, month: int) -> dict:
    month_start = date(year, month, 1).strftime("%Y-%m-%d")
    month_end = get_month_end(year, month).strftime("%Y-%m-%d")

    cashflow_data = get_cashflow_df(flow_month=str(month), flow_year=str(year))

    # Get Credit Card account info
    cashflow_data["accounts"] = get_credit_card_data(
        start=month_start, end=month_end)

    # Get Bank Account info

    return cashflow_data


def get_cashflow_chart(year: int, view_month: int, month_range: int = 6):
    chart_sql = f"""
        SELECT tran_month_name, cashflow_category, amount
        FROM vw_cashflow_chart
        WHERE tran_month_start <= ConCat('{year}-{view_month}-01')
        ORDER BY tran_month_start DESC 
        LIMIT {month_range * CASHFLOW_CHART_SEGMENTS}
    ;"""

    results = db.session.execute(text(chart_sql))

    print("cashflow chart results")

    resp = {
        'months': [
        ],
        'bot': [
        ],
        'top': [
        ],
        'total': [
        ]
    }

    for row in results:
        if row[0] not in resp['months']:
            resp['months'].append(row[0])
        resp[row[1]].append(row[2])

    return resp
