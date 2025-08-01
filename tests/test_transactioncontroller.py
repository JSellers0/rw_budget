from controllers.transactions import ctrl_transactions
from app import app

# ToDo: test all transaction controller methods

def test_transaction_insert():
    test_transaction_data = {
        'transaction_date': '2023-03-01',
        'category': 1,
        'account': 1,
        'merchant_name': 'Test Merchant',
        'transaction_type': 'credit',
        'amount': -100,
        'note': 'Test Insert'
    }
    
    with app.app_context():
        tran_res: TransactionController.TransactionResponse = TransactionController.insert_transaction(test_transaction_data)
        assert tran_res['transactions'][0].transaction.merchant_name == 'Test Merchant' # type: ignore -- need to figure out typing OR situation
        
def test_bad_credit_amount():
    test_transaction_data = {
        'transaction_date': '2023-03-02',
        'category': 1,
        'account': 2,
        'merchant_name': 'Test Merchant',
        'transaction_type': 'credit',
        'amount': 100,
        'note': 'Test insert bad credit amount'
    }
    
    with app.app_context():
        tran_res: TransactionController.TransactionResponse = TransactionController.insert_transaction(test_transaction_data)
        assert tran_res['transactions'][0].transaction.amount == -100 # type: ignore -- need to figure out typing OR situation
        
def test_pending_insert():
    test_transaction_data = {
        'transaction_date': '2023-03-02',
        'category': 1,
        'account': 2,
        'merchant_name': 'Test Merchant',
        'transaction_type': 'credit',
        'amount': -100,
        'note': 'Test insert pending transaction',
        'is_pending': 1,
    }
    
    with app.app_context():
        tran_res: TransactionController.TransactionResponse = TransactionController.insert_transaction(test_transaction_data)
        assert tran_res['transactions'][0].transaction.is_pending == 1 # type: ignore -- need to figure out typing OR situation
        
def test_get_transaction():
    with app.app_context():
        tran_res: TransactionController.TransactionResponse = TransactionController.get_transaction_by_id(1)
        assert tran_res['transactions'][0].transaction.transactionid == 1 # type: ignore -- need to figure out typing OR situation
        
def test_get_tran_by_date():
    with app.app_context():
        tran_res: TransactionController.TransactionResponse = TransactionController.get_transactions_by_date('2023-03-01')
        assert len(tran_res['transactions']) > 0