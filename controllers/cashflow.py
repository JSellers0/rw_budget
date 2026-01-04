import requests
from typing import TypedDict
from ._base import BaseController


class CashflowSummary(TypedDict):
    sum: dict[str, str] = {
        "remain": "$0.00",
        "income": "$0.00",
        "expens": "$0.00"
        }
    top: dict[str, str] = {
        "remain": "$0.00",
        "income": "$0.00",
        "expens": "$0.00"
        }
    bot: dict[str, str] = {
        "remain": "$0.00",
        "income": "$0.00",
        "expens": "$0.00"
        }

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
            if cfs.get(mg, None) is None:
                cfs.setdefault(mg, {}) 
            cfs[mg].setdefault(rec.get("cashflow_group"), rec.get("amount"))
        return cfs


