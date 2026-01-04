from app import db
from controllers.objects.models import Account
import requests
from typing import Any, TypedDict
from _base import BaseController

# ToDo: Standardize response messages
# ToDo: Response status checks where appropriate
# ToDo: try/except around db operations?

class AccountResponse(TypedDict):
    response_code: int
    message: str
    accounts: list[Account | None]

class AccountController(BaseController):
    def __init__(self):
        super.__init__(self)
        self.api_base_url += "accounts"

    def get_account_by_id(self, accountid: int) -> AccountResponse:
        uri = f"{self.api_base_url}/{accountid}"
        resp = requests.get(uri)
        
        if resp.status_code == 404:
            return AccountResponse(
                response_code=404,
                message=f"Account not found with Account ID {accountid}.",
                accounts=[None]
            )

        account = resp.json()["accounts"]

        return AccountResponse(
            response_code=200,
            message=f"Account ID {accountid} retrieved successfully",
            accounts=[account]
        )

    def get_account_by_name(self, account_name: str) -> AccountResponse:
        uri = f"{self.api_base_url}"
        resp = requests.get(uri, params={"name": account_name})
        
        if resp.status_code != 200:
            return AccountResponse(
                response_code=404,
                message=f"{account_name} does not exist.",
                accounts=[None] # type: ignore
            )
        
        accounts = resp.json()["accounts"]
        
        return AccountResponse(
                response_code=200,
                message=f"Account {account_name} retrieved successfully",
                accounts=accounts
            )
    
    def get_all_accounts(self) -> AccountResponse:
        uri = f"{self.api_base_url}"
        resp = requests.get(uri)
        
        if resp.status_code != 200:
            return AccountResponse(
                response_code=404,
                message=f"No Accounts found.",
                accounts=[None] # type: ignore
            )
        
        accounts = resp.json()["accounts"]
        
        return AccountResponse(
                response_code=200,
                message=f"Retrieved {len(accounts)} accounts.",
                accounts=accounts
            )

    def get_accounts_for_listbox(self) -> list[tuple[int, str]]:
        accounts = self.get_all_accounts()
        account_dump = [(a.accountid, a.account_name) for a in accounts]
        
        return account_dump

    def insert_account(self, account_data: dict[str, Any])-> AccountResponse:
        acct_check: Account = self.get_account_by_name(account_data.get('account_name', ''))['accounts'][0]
        
        if acct_check is not None:
            return AccountResponse(
                response_code=409,
                message=f"Account {account_data.get('account_name', '')} already exists.",
                accounts=[acct_check]
            )
        account: Account = Account(
            account_name = account_data.get('account_name', ''),
            account_type = account_data.get('account_type', ''),
            payment_day = account_data.get('payment_day', ''),
            statement_day = account_data.get('statement_day', ''),
            rewards_features = account_data.get('rewards_features', '')
            )
        
        resp = requests.post(self.api_base_url, data=account.to_json())
        
        return AccountResponse(
            response_code=200,
            message=f"Account {account_data.get('account_name', '')} insert successful.",
            accounts=[account]
        )
        

    def update_account(self, account_data: dict) -> AccountResponse:
        id_account: Account = self.get_account_by_id(account_data.get('accountid', 1))['accounts'][0]
        name_account: Account = self.get_account_by_name(account_data.get('account_name', ''))['accounts'][0]
        
        if id_account is None:
            return AccountResponse(
                response_code=404,
                message=f"No Account for Account ID {account_data.get('accountid')}.",
                accounts=[None] # type: ignore
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

    def delete_account(self, accountid: int) -> AccountResponse:
        account: Account = self.get_account_by_id(accountid)['accounts'][0]
        
        if account == None:
            return AccountResponse(
                response_code=404,
                message=f"No Account for Account ID {accountid}.",
                accounts=[None] # type: ignore
            )
        
        db.session.delete(account)
        db.session.commit()
        
        return AccountResponse(
                response_code=200,
                message=f"Account {accountid} deleted successful.",
                accounts=[account]
            )
