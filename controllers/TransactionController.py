from app import db
from controllers.models import Transaction, Transaction_Interface
from controllers.forms import TransactionForm
from datetime import date
from typing import Any

# ToDo: Should insert and update accept data_type parameter and adjust accordingly or should there be one method for each type of data?

def get_all_transactions() -> list[Transaction_Interface]:
    transactions = Transaction.query.order_by(Transaction.transaction_date.asc()).all()   
    return [Transaction_Interface(transaction, transaction.category, transaction.account) for transaction in transactions]

def get_transaction_by_id(transactionid: int) -> Transaction_Interface:
    transaction = Transaction.query.filter(Transaction.transactionid == transactionid).one_or_none()
    
    if transaction == None:
        raise ValueError(f"{transactionid} is not a valid transaction id.")
    
    return Transaction_Interface(transaction, transaction.category, transaction.account)

def get_transaction_by_date(date: str) -> list[Transaction_Interface]:
    transactions = Transaction.query.filter(Transaction.transaction_date == date).all()
    
    if len(transactions) == 0:
        raise ValueError(f"{date} does not have any transactions recorded.")
    
    return [Transaction_Interface(transaction, transaction.category, transaction.account) for transaction in transactions]

def get_transaction_by_date_range(start: str, end: str) -> list[Transaction_Interface]:
    transactions = Transaction.query.filter(Transaction.transaction_date <= end).filter(Transaction.transaction_date >= start).all()
    return [Transaction_Interface(transaction, transaction.category, transaction.account) for transaction in transactions]
    
def get_transaction_by_category(categoryid: int) -> list[Transaction_Interface]:
    transactions = Transaction.query.filter(Transaction.categoryid == categoryid).all()
    return [Transaction_Interface(transaction, transaction.category, transaction.account) for transaction in transactions]

def get_twenty_recent_transactions() -> list[Transaction_Interface]:
    transactions = Transaction.query.order_by(Transaction.transaction_date.desc()).limit(20)
    return [Transaction_Interface(transaction, transaction.category, transaction.account) for transaction in transactions]
    
def insert_transaction(transaction_data: dict) -> Transaction_Interface:
    # Make sure credit values are negative
    if transaction_data.get('transaction_type','') == 'credit':
        if transaction_data.get('amount', 0) > 0:
            transaction_data['amount'] = transaction_data['amount'] * -1
                
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
        
    return Transaction_Interface(transaction, transaction.category, transaction.account)

def insert_transaction_form(transaction_data: TransactionForm) -> Transaction_Interface:
    # Make sure credit values are negative
    if transaction_data.transaction_type.data == 'credit':
        if transaction_data.amount.data > 0: # type: ignore
            transaction_data.amount = transaction_data.amount.data * -1 # type: ignore
                
    transaction: Transaction = Transaction(
        transaction_date=transaction_data.transaction_date.data,
        accountid = transaction_data.account.data,
        categoryid=transaction_data.category.data,
        merchant_name=transaction_data.merchant_name.data,
        transaction_type=transaction_data.transaction_type.data,
        amount=transaction_data.amount.data,
        note=transaction_data.note.data
    )

    db.session.add(transaction)    
    db.session.commit()
        
    return Transaction_Interface(transaction, transaction.category, transaction.account)

def update_transaction(transaction_data: dict) -> Transaction_Interface:
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
    
    return Transaction_Interface(transaction, transaction.category, transaction.account)

def update_transaction_form(transaction_data: TransactionForm) -> Transaction_Interface:
    transaction: Transaction = Transaction.query.filter(Transaction.transactionid == transaction_data.transactionid.data).one_or_none()
    
    if transaction == None:
        raise ValueError(f"{transaction_data.transactionid.data} is not a valid transaction id.")
    
    if transaction.transaction_date != transaction_data.transaction_date.data:
        transaction.transaction_date = transaction_data.transaction_date.data # type: ignore
    if transaction_data.category.data != transaction.categoryid:
        transaction.categoryid = transaction_data.category.data # type: ignore
    if transaction_data.merchant_name.data != transaction.merchant_name:
        transaction.merchant_name = transaction_data.merchant_name.data
    if transaction_data.transaction_type.data != transaction.transaction_type:
        transaction.transaction_type = transaction_data.transaction_type.data  # type: ignore
    if transaction_data.amount.data != transaction.amount:
        transaction.amount = transaction_data.amount.data  # type: ignore
    if transaction_data.note.data != transaction.note:
        transaction.note = transaction_data.note.data

    db.session.commit()
    
    return Transaction_Interface(transaction, transaction.category, transaction.account)

def delete_transaction(transactionid: int)-> None:
    transaction = Transaction.query.filter(Transaction.transactionid == transactionid).one_or_none()
    
    if transaction == None:
        raise ValueError(f"{transactionid} is not a valid transaction id.")
    
    db.session.delete(transaction)
    db.session.commit()
    # ToDo: Does transaction object still exist and can it be assigned to Transaction_Interface?  Should it be returned?