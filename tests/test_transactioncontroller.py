from controllers import TransactionController
from app import app

def test_transaction_insert():
    test_transaction_data = {
        'transaction_date': '2023-03-01',
        'categoryid': 1,
        'merchant_name': 'Test Merchant',
        'transaction_type': 'credit',
        'amount': -100,
        'note': 'Test Insert'
    }
    
    with app.app_context():
        tran_res = TransactionController.insert_transaction(test_transaction_data).to_json()
        assert tran_res.get('merchant_name') == 'Test Merchant'
        
def test_bad_credit_amount():
    test_transaction_data = {
        'transaction_date': '2023-03-02',
        'categoryid': 1,
        'merchant_name': 'Test Merchant',
        'transaction_type': 'credit',
        'amount': 100,
        'note': 'Test insert bad credit amount'
    }
    
    with app.app_context():
        tran_res = TransactionController.insert_transaction(test_transaction_data).to_json()
        assert tran_res.get('amount') == -100
        
def test_get_transaction():
    with app.app_context():
        tran_get_res = TransactionController.get_transaction_by_id(1).to_json()
        assert tran_get_res.get('transactionid') == 1
        
def test_get_tran_by_date():
    with app.app_context():
        tran_get_res = TransactionController.get_transaction_by_date('2023-03-01')
        assert len(tran_get_res) == 1