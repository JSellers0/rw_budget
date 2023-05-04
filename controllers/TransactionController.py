from app import db
from controllers.objects.models import Transaction, TransactionInterface, RecurringTransaction
from controllers.objects.forms import TransactionForm
from datetime import date, timedelta
from typing import TypedDict
import pandas as pd

# ToDo: Get all transactions by accountid
# DECISION: Return all account transactions and let web layer filter by dates?  Or get by account and date function?
# ToDo: Standardize response messages
# ToDo: Response status checks where appropriate
# ToDo: try/except around db operations?
# ToDo: use get functions instead of repeating Transaction.query in insert,update,delete
# ToDo: Recurring transaction CRUD
# ToDo: ispending flag to all get methods
# ToDo: set ispending flag on insert/update

class TransactionResponse(TypedDict):
    response_code: int
    message: str
    transactions: list[TransactionInterface]

def get_all_transactions(is_pending:int) -> TransactionResponse:
    transactions = Transaction.query.filter(Transaction.is_pending == is_pending).order_by(Transaction.transaction_date.desc()).all()
    
    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message="No transactions found",
            transactions=[None] # type: ignore
        )
    
    return TransactionResponse(
            response_code=200,
            message=f"Retrieved {len(transactions)} transactions.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account) for transaction in transactions]
        )

def get_transaction_by_id(transactionid: int) -> TransactionResponse:
    transaction = Transaction.query.filter(Transaction.transactionid == transactionid).one_or_none()
    
    if transaction == None:
        return TransactionResponse(
            response_code=404,
            message="No transactions found",
            transactions=[None] # type: ignore
        )
    
    return TransactionResponse(
            response_code=200,
            message=f"Successfully retrieved transaction {transactionid}.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account)]
        )

def get_transactions_by_date(date: str) -> TransactionResponse:
    transactions = Transaction.query.filter(Transaction.transaction_date == date).all()
    
    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message=f"No transactions found on {date}",
            transactions=[None] # type: ignore
        )
    
    return TransactionResponse(
            response_code=200,
            message=f"Retrieved {len(transactions)} on {date}.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account) for transaction in transactions]
        )

def get_transactions_by_date_range(start: str, end: str) -> TransactionResponse:
    transactions = Transaction.query.filter(Transaction.transaction_date <= end).filter(Transaction.transaction_date >= start).all()
    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message=f"No transactions found between {start} and {end}",
            transactions=[None] # type: ignore
        )
    
    return TransactionResponse(
            response_code=200,
            message=f"Retrieved {len(transactions)} between {start} and {end}.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account) for transaction in transactions]
    )
    
def get_transactions_by_category(categoryid: int) -> TransactionResponse:
    transactions = Transaction.query.filter(Transaction.categoryid == categoryid).all()
    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message=f"No transactions found for category {categoryid}",
            transactions=[None] # type: ignore
        )
    
    return TransactionResponse(
            response_code=200,
            message=f"Retrieved {len(transactions)} for category {categoryid}.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account) for transaction in transactions]
    )

def get_twenty_recent_transactions() -> TransactionResponse:
    transactions = Transaction.query.order_by(Transaction.transaction_date.desc()).limit(20)
    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message=f"No transactions found.",
            transactions=[None] # type: ignore
        )
    
    return TransactionResponse(
            response_code=200,
            message=f"Retrieved {len(transactions)}.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account) for transaction in transactions]
    )
    
def insert_transaction(transaction_data: dict) -> TransactionResponse:
    # Make sure credit values are negative
    if transaction_data.get('transaction_type','') == 'credit':
        if transaction_data.get('amount', 0) > 0:
            transaction_data['amount'] = transaction_data['amount'] * -1
            
    # ToDo: Check for record with the exact same values?
                
    transaction: Transaction = Transaction(
        transaction_date=transaction_data.get('transaction_date', date.today()),
        merchant_name=transaction_data.get('merchant_name', ''),
        categoryid=transaction_data.get('category', 1),
        amount=transaction_data.get('amount', 0),
        accountid=transaction_data.get('account', 1),
        transaction_type=transaction_data.get('transaction_type', ''),
        note=transaction_data.get('note', ''),
        is_pending=transaction_data.get('is_pending', 0)
    )

    db.session.add(transaction)    
    db.session.commit()
    
    return TransactionResponse(
            response_code=200,
            message=f"Transaction insert successful.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account)]
    )

def update_transaction(transaction_data: dict) -> TransactionResponse:
    transaction: Transaction = Transaction.query.filter(Transaction.transactionid == transaction_data.get('transactionid')).one_or_none()
    
    if transaction == None:
        return TransactionResponse(
            response_code=404,
            message=f"Transaction { transaction_data.get('transactionid')} not found.",
            transactions=[None] # type: ignore
        )
    
    if transaction_data.get('transaction_date') != transaction.transaction_date:
        transaction.transaction_date = transaction_data.get('transaction_date', '') # type: ignore
    if transaction_data.get('merchant_name') != transaction.merchant_name:
        transaction.merchant_name = transaction_data.get('merchant_name', '') # type: ignore
    if transaction_data.get('category') != transaction.categoryid:
        transaction.categoryid = transaction_data.get('category', 1) # type: ignore
    if transaction_data.get('amount') != transaction.amount:
        transaction.amount = transaction_data.get('amount', 0) # type: ignore
    if transaction_data.get('account') != transaction.accountid:
        transaction.accountid = transaction_data.get('account', 0) # type: ignore
    if transaction_data.get('transaction_type') != transaction.transaction_type:
        transaction.transaction_type = transaction_data.get('transaction_type', '') # type: ignore
    if transaction_data.get('is_pending') != transaction.is_pending:
        transaction.is_pending = transaction_data.get('is_pending', 1) # type: ignore
    if transaction_data.get('note') != transaction.note:
        transaction.note = transaction_data.get('note', '') # type: ignore
    
    db.session.commit()
    
    return TransactionResponse(
            response_code=200,
            message=f"Transaction insert successful.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account)]
    )

def delete_transaction(transactionid: int)-> TransactionResponse:
    transaction = Transaction.query.filter(Transaction.transactionid == transactionid).one_or_none()
    
    if transaction == None:
        raise ValueError(f"{transactionid} is not a valid transaction id.")
    
    transactions=[TransactionInterface(transaction, transaction.category, transaction.account)]
    
    db.session.delete(transaction)
    db.session.commit()
    
    return TransactionResponse(
            response_code=200,
            message=f"Transaction {transactionid} deleted successfully.",
            transactions=transactions
    )
    
def get_all_recurring_transactions() -> TransactionResponse:
    r_trans = RecurringTransaction.query.order_by(RecurringTransaction.expected_day.asc()).all()
    return TransactionResponse(
            response_code=200,
            message=f"Retrieved {len(r_trans)} recurring transactions.",
            transactions=[TransactionInterface(r_tran, r_tran.category, r_tran.account) for r_tran in r_trans]
        )
    
def get_rtran_by_id(rtranid: int) -> TransactionResponse:
    r_tran = RecurringTransaction.query.filter(RecurringTransaction.rtranid == rtranid).one_or_none()
    
    if r_tran == None:
        return TransactionResponse(
            response_code=404,
            message="No transactions found",
            transactions=[None] # type: ignore
        )
    
    return TransactionResponse(
            response_code=200,
            message=f"Successfully retrieved transaction {rtranid}.",
            transactions=[TransactionInterface(r_tran, r_tran.category, r_tran.account)]
        )
    
def insert_recurring_transaction(transaction_data: dict) -> TransactionResponse:          
    # Make sure credit values are negative
    if transaction_data.get('transaction_type','') == 'credit':
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
            message=f"Transaction insert successful.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account)]
    )
    
def update_recurring_transaction(transaction_data: dict) -> TransactionResponse:
    transaction: RecurringTransaction = RecurringTransaction.query.filter(RecurringTransaction.rtranid == transaction_data.get('rtranid')).one_or_none()
    
    if transaction == None:
        return TransactionResponse(
            response_code=404,
            message=f"Transaction { transaction_data.get('rtranid')} not found.",
            transactions=[None] # type: ignore
        )
            
    if transaction_data.get('expected_day') != transaction.expected_day:
        transaction.expected_day = transaction_data.get('expected_day', '') # type: ignore
    if transaction_data.get('merchant_name') != transaction.merchant_name:
        transaction.merchant_name = transaction_data.get('merchant_name', '') # type: ignore
    if transaction_data.get('category') != transaction.categoryid:
        transaction.categoryid = transaction_data.get('category', 1) # type: ignore
    if transaction_data.get('amount') != transaction.amount:
        transaction.amount = transaction_data.get('amount', 0) # type: ignore
    if transaction_data.get('account') != transaction.accountid:
        transaction.accountid = transaction_data.get('account', 0) # type: ignore
    if transaction_data.get('transaction_type') != transaction.transaction_type:
        transaction.transaction_type = transaction_data.get('transaction_type', '') # type: ignore
    if transaction_data.get('is_monthly') != transaction.is_monthly:
        transaction.is_monthly = transaction_data.get('is_monthly', True) # type: ignore
    if transaction_data.get('note') != transaction.note:
        transaction.note = transaction_data.get('note', '') # type: ignore
    
    db.session.commit()
    
    return TransactionResponse(
            response_code=200,
            message=f"Transaction insert successful.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account)]
    )

def apply_recurring_transactions(rtrans_data) -> TransactionResponse:
    transactions = []
    for rtranid in rtrans_data.get("RTranIDs").split(","):
        # ToDo: Check Response
        get_rtran_response = get_rtran_by_id(int(rtranid))
        rtran = get_rtran_response['transactions'][0]
        tran_data = {
            "transaction_date": date(year=date.today().year, month=rtrans_data.get('month'), day=rtran.transaction.expected_day), # type: ignore
            "merchant_name": rtran.transaction.merchant_name, # type: ignore
            "category": rtran.transaction.categoryid, # type: ignore
            "amount": rtran.transaction.amount, # type: ignore
            "account": rtran.transaction.accountid, # type: ignore
            "transaction_type": rtran.transaction.transaction_type, # type: ignore
            "note": rtran.transaction.note, # type: ignore
            "is_pending": 1
        }
        # ToDo: Check Response
        tran_insert_response = insert_transaction(transaction_data=tran_data)
        transactions.append(tran_insert_response['transactions'][0])
        
    return TransactionResponse(
        response_code=200,
        message=f"Successfully inserted {len(transactions)} recurring transactions.",
        transactions=transactions
    )
    
def get_month_end(year:int, month: int) -> date:
    if month == 12:
        next_month = 1
        year = year + 1
    else:
        next_month = month + 1
        year = year
    return date(year, next_month, 1) - timedelta(days=1)
    
def get_cashflow_df(year:int, month:int) -> pd.DataFrame:
    start = date(year, month, 1).strftime("%Y-%m-%d")
    end = get_month_end(year, month).strftime("%Y-%m-%d")
    get_response = get_transactions_by_date_range(start=start, end=end)
    
    if get_response["response_code"] == 404:
        return pd.DataFrame()
    
    cashflow_transactions = []
    for transaction in get_response['transactions']:
        cashflow_transactions.append({
            "transactionid": transaction.transaction.transactionid,
            "transaction_date": transaction.transaction.transaction_date,
            "merchant_name": transaction.transaction.merchant_name,
            "category": transaction.category.category_name,
            "amount": transaction.transaction.amount,
            "account": transaction.account.account_name,
            "account_type": transaction.account.account_type,
            "transaction_type": transaction.transaction.transaction_type,
            "is_pending": transaction.transaction.is_pending,
        })
        
    cashflow_df = pd.DataFrame.from_records(
        cashflow_transactions,
        index="transactionid",
        columns=cashflow_transactions[0].keys()
    )
    
    return cashflow_df
    
def get_cashflow(year:int, month:int) -> dict:   
    cashflow_data = {
        "sum": {
            "remain": '$0.00',
            "income": '$0.00',
            "expens": '$0.00',
        },
        "top": {
            "remain": '$0.00',
            "income": '$0.00',
            "expens": '$0.00',
            "accounts": pd.DataFrame(),
        },
        "bot": {
            "remain": '$0.00',
            "income": '$0.00',
            "expens": '$0.00',
            "accounts": pd.DataFrame(),
        }
    }
    
    cashflow_df = get_cashflow_df(year=year, month=month)
    
    if len(cashflow_df) == 0:
        return cashflow_data
     
    top_df = cashflow_df.loc[cashflow_df["transaction_date"] < date(year, month, 15)]
    bot_df = cashflow_df.loc[cashflow_df["transaction_date"] > date(year, month, 14)]
    
    cashflow_data["sum"]["remain"] = '${:0,.2f}'.format(cashflow_df[["amount"]].sum().amount)
    cashflow_data["top"]["remain"] = '${:0,.2f}'.format(top_df[["amount"]].sum().amount)
    cashflow_data["bot"]["remain"] = '${:0,.2f}'.format(bot_df[["amount"]].sum().amount)
    
    cashflow_data["sum"]["income"] = '${:0,.2f}'.format(cashflow_df.loc[cashflow_df["category"] == "Income"][["amount"]].sum().amount)
    cashflow_data["top"]["income"] = '${:0,.2f}'.format(top_df.loc[top_df["category"] == "Income"][["amount"]].sum().amount)
    cashflow_data["bot"]["income"] = '${:0,.2f}'.format(bot_df.loc[bot_df["category"] == "Income"][["amount"]].sum().amount)
    
    cashflow_data["sum"]["expens"] = '${:0,.2f}'.format(cashflow_df.loc[
        (cashflow_df["transaction_type"] == "credit") &
        (~cashflow_df["category"].isin(["Transfer","Card Payment"]))
        ][["amount"]].sum().amount)
    cashflow_data["top"]["expens"] = '${:0,.2f}'.format(top_df.loc[
        (top_df["transaction_type"] == "credit") &
        (~top_df["category"].isin(["Transfer","Card Payment"]))
        ][["amount"]].sum().amount)
    cashflow_data["bot"]["expens"] = '${:0,.2f}'.format(bot_df.loc[
        (bot_df["transaction_type"] == "credit") &
        (~bot_df["category"].isin(["Transfer","Card Payment"]))
        ][["amount"]].sum().amount)
    
    top_accounts = top_df.loc[top_df.account_type == "Credit Card"]
    bot_accounts = bot_df.loc[bot_df.account_type == "Credit Card"]
    
    cashflow_data["top"]["accounts"] = top_accounts[["account"]].drop_duplicates()
    cashflow_data["bot"]["accounts"] = bot_accounts[["account"]].drop_duplicates()
    
    print("=================top accounts======================")
    print(top_accounts)
    print(cashflow_data["top"]["accounts"])
    
    # Current Charges
    top_acct_chg_bal = top_accounts.loc[
        (top_accounts["is_pending"] == 0) & (top_accounts["transaction_type"] == 'credit')
        ][["account", "amount"]].groupby("account").sum().reset_index()
    
    if len(top_acct_chg_bal):
        cashflow_data["top"]["accounts"] = pd.merge(
            cashflow_data["top"]["accounts"],
            top_acct_chg_bal,
            on="account",
            how="left"
        ).rename(columns={"amount": "chg_bal"})
    else:
        cashflow_data["top"]["accounts"]["chg_bal"] = 0
    
    bot_acct_chg_bal = bot_accounts.loc[
        (bot_accounts["is_pending"] == 0) & (bot_accounts["transaction_type"] == 'credit')
        ][["account", "amount"]].groupby("account").sum().reset_index()
    
    if len(bot_acct_chg_bal):
        cashflow_data["bot"]["accounts"] = pd.merge(
            cashflow_data["bot"]["accounts"],
            bot_acct_chg_bal,
            on="account",
            how="left"
        ).rename(columns={"amount": "chg_bal"})
    else:
        cashflow_data["bot"]["accounts"]["chg_bal"] = 0
    
    # Pending Balance
    top_acct_pnd_bal = top_accounts.loc[
        (top_accounts["transaction_type"] == 'credit')
        ][["account", "amount"]].groupby("account").sum().reset_index()
    
    if len(top_acct_pnd_bal):
        cashflow_data["top"]["accounts"] = pd.merge(
            cashflow_data["top"]["accounts"],
            top_acct_pnd_bal,
            on="account",
            how="left"
        ).rename(columns={"amount": "pnd_bal"})
    else:
        cashflow_data["top"]["accounts"]["pnd_bal"] = 0
        
    bot_acct_pnd_bal = bot_accounts.loc[
        (bot_accounts["is_pending"] == 0) & (bot_accounts["transaction_type"] == 'credit')
        ][["account", "amount"]].groupby("account").sum().reset_index()
    
    if len(bot_acct_pnd_bal):
        cashflow_data["bot"]["accounts"] = pd.merge(
            cashflow_data["bot"]["accounts"],
            bot_acct_pnd_bal,
            on="account",
            how="left"
        ).rename(columns={"amount": "pnd_bal"})
    else:
        cashflow_data["bot"]["accounts"]["pnd_bal"] = 0
    
    # Payments
    top_acct_payments = top_accounts.loc[
        (top_accounts["transaction_type"] == 'debit')
        ][["account", "amount"]].groupby("account").sum().reset_index()
    
    if len(top_acct_payments):
        cashflow_data["top"]["accounts"] = pd.merge(
            cashflow_data["top"]["accounts"],
            top_acct_payments,
            on="account",
            how="left"
        ).rename(columns={"amount": "pmt_bal"})
    else:
        cashflow_data["top"]["accounts"]["pmt_bal"] = 0
        
    bot_acct_payments = bot_accounts.loc[
        (bot_accounts["transaction_type"] == 'debit')
        ][["account", "amount"]].groupby("account").sum().reset_index()
    
    if len(bot_acct_payments):
        cashflow_data["bot"]["accounts"] = pd.merge(
            cashflow_data["bot"]["accounts"],
            bot_acct_payments,
            on="account",
            how="left"
        ).rename(columns={"amount": "pmt_bal"})
    else:
        cashflow_data["bot"]["accounts"]["pmt_bal"] = 0
        
    # Current Balance
    top_acct_cur_bal = top_accounts.loc[
        (top_accounts["is_pending"] == 0)
        ][["account", "amount"]].groupby("account").sum().reset_index()
    
    if len(top_acct_cur_bal):
        cashflow_data["top"]["accounts"] = pd.merge(
            cashflow_data["top"]["accounts"],
            top_acct_cur_bal,
            on="account",
            how="left"
        ).rename(columns={"amount": "cur_bal"})
    else:
        cashflow_data["top"]["accounts"]["cur_bal"] = 0
    
    bot_acct_cur_bal = bot_accounts.loc[
        (bot_accounts["is_pending"] == 0)
        ][["account", "amount"]].groupby("account").sum().reset_index()
    
    if len(bot_acct_cur_bal):
        cashflow_data["bot"]["accounts"] = pd.merge(
            cashflow_data["bot"]["accounts"],
            bot_acct_cur_bal,
            on="account",
            how="left"
        ).rename(columns={"amount": "cur_bal"})
    else:
        cashflow_data["bot"]["accounts"]["cur_bal"] = 0
    
    # Fill NAs
    cashflow_data["top"]["accounts"].fillna(0, inplace=True)
    cashflow_data["bot"]["accounts"].fillna(0, inplace=True)
       
    return cashflow_data