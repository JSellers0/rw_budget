from app import db
from controllers.objects.models import Account
from controllers.objects.forms import AccountForm
from typing import Any, TypedDict

# ToDo: Standardize response messages
# ToDo: Response status checks where appropriate
# ToDo: try/except around db operations?

class AccountResponse(TypedDict):
    response_code: int
    message: str
    accounts: list[Account]

def get_account_by_id(accountid: int) -> AccountResponse:
    account: Account = Account.query.filter(Account.accountid == accountid).one_or_none()
    
    if account == None:
        return AccountResponse(
            response_code=404,
            message=f"Account not found with Account ID {accountid}.",
            accounts=[None]
        )
    
    return AccountResponse(
            response_code=200,
            message=f"Account ID {accountid} retrieved successfully",
            accounts=[account]
        )

def get_account_by_name(account_name: str) -> AccountResponse:
    account: Account = Account.query.filter(str(Account.account_name).lower() == account_name.lower()).one_or_none()
    
    if account == None:
        return AccountResponse(
            response_code=404,
            message=f"{account_name} does not exist.",
            accounts=[None]
        )
    
    return AccountResponse(
            response_code=200,
            message=f"Account {account_name} retrieved successfully",
            accounts=[account]
        )
    
def get_all_accounts() -> AccountResponse:
    accounts = Account.query.order_by(Account.account_type).all()
    
    if len(accounts) == 0:
        return AccountResponse(
            response_code=404,
            message=f"No Accounts found.",
            accounts=[None]
        )
    
    return AccountResponse(
            response_code=200,
            message=f"Retrieved {len(accounts)} accounts.",
            accounts=[account for account in accounts]
        )

def get_accounts_for_listbox() -> list[tuple[int, str]]:
    accounts = Account.query.all()
    account_dump = [account.to_tuple() for account in accounts]
    
    return account_dump

def insert_account(account_data: dict[str, Any])-> AccountResponse:
    acct_check: Account = get_account_by_name(account_data.get('account_name', ''))['accounts'][0]
    
    if acct_check is None:
        account: Account = Account(
            account_name = account_data.get('account_name', ''),
            account_type = account_data.get('account_type', ''),
            payment_day = account_data.get('payment_day', ''),
            statement_day = account_data.get('statement_day', ''),
            rewards_features = account_data.get('rewards_features', '')
            )
        
        db.session.add(account)
        db.session.commit()
        
        return AccountResponse(
            response_code=200,
            message=f"Account {account_data.get('account_name', '')} insert successful.",
            accounts=[account]
        )
        
    return AccountResponse(
            response_code=409,
            message=f"Account {account_data.get('account_name', '')} already exists.",
            accounts=[acct_check]
        )

def update_account(account_data: dict) -> AccountResponse:
    id_account: Account = get_account_by_id(account_data.get('accountid', 1))['accounts'][0]
    name_account: Account = get_account_by_name(account_data.get('account_name', ''))['accounts'][0]
    
    if id_account is None:
        return AccountResponse(
            response_code=404,
            message=f"No Account for Account ID {account_data.get('accountid')}.",
            accounts=[None]
        )
    
    # If the user is trying to change the account name and it already exists, then let them know an account with
    # that name already exists.
    if account_data.get('account_name', '').lower() != id_account.account_name.lower() and name_account is not None:
        return AccountResponse(
            response_code=409,
            message=f"Account {account_data.get('account_name', '')} already exists.",
            accounts=[name_account]
        )
    
    id_account.account_name = account_data.get('account_name', '')
    id_account.account_type = account_data.get('account_type', '')
    id_account.rewards_features = account_data.get('rewards_features', '')
    id_account.payment_day = account_data.get('payment_day', '')
    id_account.statement_day = account_data.get('statement_day', '')
    
    db.session.commit()
    
    return AccountResponse(
            response_code=200,
            message=f"Account {id_account.accountid} update successful.",
            accounts=[id_account]
        )

def delete_account(accountid: int) -> AccountResponse:
    account: Account = get_account_by_id(accountid)['accounts'][0]
    
    if account == None:
        return AccountResponse(
            response_code=404,
            message=f"No Account for Account ID {accountid}.",
            accounts=[None]
        )
    
    db.session.delete(account)
    db.session.commit()
    
    return AccountResponse(
            response_code=200,
            message=f"Account {accountid} deleted successful.",
            accounts=[account]
        )
     
     