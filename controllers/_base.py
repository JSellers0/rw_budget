from dataclasses import dataclass

@dataclass
class ControllerResponse:
    response_code: str
    message: str