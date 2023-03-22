from app import db
from controllers.models import Account
from controllers.forms import AccountForm
from typing import Any

def get_account_by_id(accountid: int) -> Account:
    account: Account = Account.query.filter(Account.accountid == accountid).one_or_none()
    
    if account == None:
        raise ValueError(f"{accountid} is not a valid account id.")
    
    return account

def get_account_by_name(account_name: str) -> Account:
    account: Account = Account.query.filter(Account.account_name == account_name).one_or_none()
    
    if account == None:
        raise ValueError(f"{account_name} does not exist.")
    
    return account
    
def get_all_accounts() -> list[dict[str, Any]]:
    accounts = Account.query.order_by(Account.account_type).all()
    account_dump = [account.to_json() for account in accounts]
    
    return account_dump

def get_accounts_for_listbox() -> list[tuple[int, str]]:
    accounts = Account.query.all()
    account_dump = [account.to_tuple() for account in accounts]
    
    return account_dump

def insert_account(account_data: AccountForm)-> Account:
    # ToDo: Check for account name existing already.
    account: Account = Account(
        account_name = account_data.account_name.data,
        account_type = account_data.account_type.data,
        payment_day = account_data.payment_day.data,
        statement_day = account_data.statement_day.data,
        rewards_features = account_data.rewards_features.data
        )
    
    db.session.add(account)
    db.session.commit()
    
    return account

def update_account(account_data: dict) -> Account:
    # ToDo: Check for account name existing already.
    account: Account = Account.query.filter(Account.accountid == account_data.get('accountid')).one_or_none()
    
    if account == None:
        raise ValueError(f"{account_data.get('accountid')} is not a valid account id.")
    
    if account_data.get('account_name') != account.account_name:
        account.account_name = account_data.get('account_name', '').lower() # type: ignore
    
    db.session.commit()
    
    return account

def delete_account(accountid: int) -> None:
    account: Account = Account.query.filter(Account.accountid == accountid).one_or_none()
    
    if account == None:
        raise ValueError(f"{accountid} is not a valid account id.")
    
    db.session.delete(account)
    db.session.commit()
     
     