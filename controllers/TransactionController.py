from app import db
from controllers.models import Transaction, Category
from datetime import date
from typing import Any

def get_all_transactions() -> list[dict[str, Any]]:
    transactions = Transaction.query.order_by(Transaction.transaction_date.asc()).all()
    transaction_dump = [transaction.to_json(transaction.category.category_name) for transaction in transactions]
    
    return transaction_dump

def get_transaction_by_id(transactionid: int) -> Transaction:
    transaction = Transaction.query.filter(Transaction.transactionid == transactionid).one_or_none()
    
    if transaction == None:
        raise ValueError(f"{transactionid} is not a valid transaction id.")
    
    return transaction

def get_transaction_by_date(date: str) -> list[dict[str, Any]]:
    transactions = Transaction.query.filter(Transaction.transaction_date == date)
    transaction_dump = [transaction.to_json(transaction.category.category_name) for transaction in transactions]
    
    if len(transaction_dump) == 0:
        raise ValueError(f"{date} does not have any transactions recorded.")
    
    return transaction_dump

def get_transaction_by_date_range(start: str, end: str) -> list[Any]:
    transactions = Transaction.query.filter(Transaction.transaction_date <= end).filter(Transaction.transaction_date >= start)
    transaction_dump = [transaction.to_json(transaction.category.category_name) for transaction in transactions]
    
    return transaction_dump
    
def get_transaction_by_category(categoryid: int) -> list[Any]:
    transactions = Transaction.query.filter(Transaction.categoryid <= categoryid)
    transaction_dump = [transaction.to_json(transaction.category.category_name) for transaction in transactions]
    
    return transaction_dump

def get_twenty_recent_transactions() -> list[Any]:
    transactions = Transaction.query.order_by(Transaction.transaction_date.desc()).limit(20)
    transaction_dump = [transaction.to_json(transaction.category.category_name) for transaction in transactions]
    
    return transaction_dump
    
def insert_transaction(transaction_data: dict) -> Transaction:
    # Make sure credit values are negative
    if transaction_data.get('transaction_type','') == 'credit':
        if transaction_data.get('amount', 0) > 0:
            transaction_data['amount'] = transaction_data['amount'] * -1
                
    transaction: Transaction = Transaction(
        transaction_date=transaction_data.get('transaction_date', date.today()),
        categoryid=transaction_data.get('categoryid', 1),
        merchant_name=transaction_data.get('merchant_name', ''),
        transaction_type=transaction_data.get('transaction_type', ''),
        amount=transaction_data.get('amount', 0),
        note=transaction_data.get('note', '')
    )

    db.session.add(transaction)    
    db.session.commit()
        
    return transaction

def update_transaction(transaction_data: dict) -> Transaction:
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
    
    return transaction

def delete_transaction(transactionid: int)-> None:
    transaction = Transaction.query.filter(Transaction.transactionid == transactionid).one_or_none()
    
    if transaction == None:
        raise ValueError(f"{transactionid} is not a valid transaction id.")
    
    db.session.delete(transaction)
    db.commit()