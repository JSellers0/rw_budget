import controllers.models.transaction as tr
from app import db

def insert_transaction(transaction_data: dict) -> tr.Transaction:
    if transaction_data.get('transaction_type','') == 'credit':
        if transaction_data.get('amount', 0) > 0:
            transaction_data['amount'] = transaction_data['amount'] * -1
            
    transaction = tr.Transaction(
        transaction_date=transaction_data.get('transaction_date'),
        categoryid=transaction_data.get('categoryid', 1),
        merchant_name=transaction_data.get('merchant_name', ''),
        transaction_type=transaction_data.get('transaction_type', ''),
        amount=transaction_data.get('amount', 0),
        note=transaction_data.get('note', '')
    )
    
    db.session.add(transaction)    
    db.session.commit()
        
    return transaction

def get_transaction_by_id(transactionid: int) -> tr.Transaction:
    transaction = tr.Transaction.query.filter(tr.Transaction.transactionid == transactionid).one_or_none()
    
    return transaction

def get_transaction_by_date(date: str):
    transactions = tr.Transaction.query.filter(tr.Transaction.transaction_date == date)
    transaction_dump = [transaction.to_json() for transaction in transactions]
    
    return transaction_dump
    

