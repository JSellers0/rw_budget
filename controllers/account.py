from app import db
from controllers.objects.models import Account
import requests
from typing import Any, TypedDict
from ._base import BaseController

# ToDo: Standardize response messages
# ToDo: Response status checks where appropriate
# ToDo: try/except around db operations?

class AccountResponse(TypedDict):
    response_code: int
    message: str
    accounts: list[Account | None]

class AccountController(BaseController):
    def __init__(self):
        super().__init__()
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

        account = Account(**resp.json()["accounts"])

        return AccountResponse(
            response_code=200,
            message=f"Account ID {accountid} retrieved successfully",
            accounts=[account]
        )

    def get_account_by_name(self, account_name: str) -> AccountResponse:
        uri = f"{self.api_base_url}/"
        resp = requests.get(uri, params={"name": account_name})
        
        if resp.status_code != 200:
            return AccountResponse(
                response_code=404,
                message=f"{account_name} does not exist.",
                accounts=[None] # type: ignore
            )
        
        accounts: list[Account] = []
        for record in resp.json()["accounts"]:
            accounts.append(Account(**record))
        
        return AccountResponse(
                response_code=200,
                message=f"Account {account_name} retrieved successfully",
                accounts=accounts
            )
    
    def get_all_accounts(self) -> AccountResponse:
        uri = f"{self.api_base_url}/"
        resp = requests.get(uri)
        
        if resp.status_code != 200:
            return AccountResponse(
                response_code=404,
                message=f"No Accounts found.",
                accounts=[None] # type: ignore
            )
        
        accounts: list[Account] = []
        for record in resp.json()["accounts"]:
            accounts.append(Account(**record))
        
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
        account: Account = Account(**account_data)        
        resp = requests.post(self.api_base_url, data=account.to_json())
        
        return AccountResponse(
            response_code=200,
            message=f"Account {account_data.get('account_name', '')} insert successful.",
            accounts=[account]
        )
        

    def update_account(self, account_data: dict) -> AccountResponse:
        accountid = account_data.get("accountid")
        uri = f"{self.api_base_url}/{account_data.get("accountid")}"
        resp = requests.put(uri, data=account_data)

        if resp.status_code != 200:
            return AccountResponse(
                response_code=404,
                message=f"No Account for Account ID {account_data.get('accountid')}.",
                accounts=[None]
            )
        
        return AccountResponse(
                response_code=200,
                message=f"Account {accountid} update successful.",
                accounts=[Account(**account_data)]
            )

    def delete_account(self, accountid: int) -> AccountResponse:
        uri = f"{self.api_base_url}/{accountid}"
        resp = requests.delete(uri)
        
        if resp.status_code != 200:
            return AccountResponse(
                response_code=resp.status_code,
                message=resp.json()["message"],
                accounts=[None]
            )
        
        return AccountResponse(
                response_code=200,
                message=f"Account {accountid} deleted successful.",
                accounts=[None]
            )
