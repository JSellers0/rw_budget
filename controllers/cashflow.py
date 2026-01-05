import requests
from ._base import BaseController


class CashflowSummary:
    def __init__(self):
        self.data = {
            "sum": {
                "remain": "0.00",
                "income": "0.00",
                "expens": "0.00",
            },
            "top": {
                "remain": "0.00",
                "income": "0.00",
                "expens": "0.00",
            },
            "bot": {
                "remain": "0.00",
                "income": "0.00",
                "expens": "0.00",
            },
        }

    def get(self, key: str) -> dict:
        return self.data.get(key, {})


class CashflowChart:
    def __init__(self):
        self.data = {
            "months": [],
            "bot": [],
            "top": [],
            "total": []
        }

    def get(self, key: str) -> list:
        return self.data.get(key, [])


class CashflowController(BaseController):
    def __init__(self):
        super().__init__()
        self.api_base_url += "cashflows"

    def get_cf_summary(self, year: int, month: int) -> CashflowSummary:
        uri = f"{self.api_base_url}/summary/{year}/{month}"
        resp = requests.get(uri)

        cfs = CashflowSummary()
        for rec in resp.json()["cashflows"]:
            mg = rec.get("month_group")
            cfs.get(mg)[rec.get("cashflow_group")] = f"{rec.get("amount"):,}"
        return cfs.data

    def get_cf_chart(self, year: int, month: int) -> CashflowChart:
        uri = f"{self.api_base_url}/chart/{year}/{month}"
        resp = requests.get(uri)
        cfc = CashflowChart()
        for record in resp.json()["chart"]:
            if record["tran_month_name"] not in cfc.get('months'):
                cfc.get("months").append(record["tran_month_name"])
            cfc.get(record["cashflow_category"]).append(record["amount"])

        return cfc.data

    def get_cf_cards(self, year: int, month: int) -> dict:
        uri = f"{self.api_base_url}/card_balances/{year}/{month}"
        resp = requests.get(uri)
        print("Card Balances: ", resp.json())

        if resp.status_code != 200:
            pass    
            
        return resp.json()
