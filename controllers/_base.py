from dataclasses import dataclass
from os import environ

@dataclass
class ControllerResponse:
    response_code: str
    message: str

class BaseController:
    def __init__(self):
        self.api_base_url = f"{environ.get("API_BASE_URL")}/{environ.get("API_VERSION")}/"