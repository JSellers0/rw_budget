from app import db
from controllers.objects.models import Transaction, TransactionInterface, RecuringTransaction, RecurringTransactionInterface
from controllers.objects.forms import TransactionForm
from datetime import date
from typing import TypedDict

# ToDo: Get all transactions by accountid
# DECISION: Return all account transactions and let web layer filter by dates?  Or get by account and date function?
# ToDo: Standardize response messages
# ToDo: Response status checks where appropriate
# ToDo: try/except around db operations?
# ToDo: use get functions instead of repeating Transaction.query in insert,update,delete
# ToDo: Recurring transaction CRUD

class TransactionResponse(TypedDict):
    response_code: int
    message: str
    transactions: list[TransactionInterface | RecurringTransactionInterface | None]

def get_all_transactions() -> TransactionResponse:
    transactions = Transaction.query.order_by(Transaction.transaction_date.asc()).all()
    
    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message="No transactions found",
            transactions=[None]
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
            transactions=[None]
        )
    
    return TransactionResponse(
            response_code=200,
            message=f"Successfully retrieved transaction {transactionid}.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account)]
        )

def get_transaction_by_date(date: str) -> TransactionResponse:
    transactions = Transaction.query.filter(Transaction.transaction_date == date).all()
    
    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message=f"No transactions found on {date}",
            transactions=[None]
        )
    
    return TransactionResponse(
            response_code=200,
            message=f"Retrieved {len(transactions)} on {date}.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account) for transaction in transactions]
        )

def get_transaction_by_date_range(start: str, end: str) -> TransactionResponse:
    transactions = Transaction.query.filter(Transaction.transaction_date <= end).filter(Transaction.transaction_date >= start).all()
    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message=f"No transactions found between {start} and {end}",
            transactions=[None]
        )
    
    return TransactionResponse(
            response_code=200,
            message=f"Retrieved {len(transactions)} between {start} and {end}.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account) for transaction in transactions]
    )
    
def get_transaction_by_category(categoryid: int) -> TransactionResponse:
    transactions = Transaction.query.filter(Transaction.categoryid == categoryid).all()
    if len(transactions) == 0:
        return TransactionResponse(
            response_code=404,
            message=f"No transactions found for category {categoryid}",
            transactions=[None]
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
            transactions=[None]
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
        accountid=transaction_data.get('accountid', 1),
        categoryid=transaction_data.get('categoryid', 1),
        merchant_name=transaction_data.get('merchant_name', ''),
        transaction_type=transaction_data.get('transaction_type', ''),
        amount=transaction_data.get('amount', 0),
        note=transaction_data.get('note', '')
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
        raise ValueError(f"{transaction_data.get('transactionid')} is not a valid transaction id.")
    
    if transaction_data.get('transaction_date') != transaction.transaction_date:
        transaction.transaction_date = transaction_data.get('transaction_date', '')
    if transaction_data.get('categoryid') != transaction.categoryid:
        transaction.categoryid = transaction_data.get('categoryid', 1)
    if transaction_data.get('merchant_name') != transaction.merchant_name:
        transaction.merchant_name = transaction_data.get('merchant_name', '')
    if transaction_data.get('transaction_type') != transaction.transaction_type:
        transaction.transaction_type = transaction_data.get('transaction_type', '')
    if transaction_data.get('amount') != transaction.amount:
        transaction.amount = transaction_data.get('amount', 0)
    if transaction_data.get('note') != transaction.note:
        transaction.note = transaction_data.get('note', '')

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
    
    db.session.delete(transaction)
    db.session.commit()
    
    return TransactionResponse(
            response_code=200,
            message=f"Transaction {transactionid} deleted successfully.",
            transactions=[TransactionInterface(transaction, transaction.category, transaction.account)]
    )
    
def get_all_recurring_transactions() -> TransactionResponse:
    r_trans = RecuringTransaction.query.order_by(RecuringTransaction.expected_day.asc()).all()
    return TransactionResponse(
            response_code=200,
            message=f"Retrieved {len(r_trans)} recurring transactions.",
            transactions=[RecurringTransactionInterface(r_tran, r_tran.interval, r_tran.category, r_tran.account) for r_tran in r_trans]
        )