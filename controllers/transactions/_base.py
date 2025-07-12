
from dataclasses import dataclass
from ..objects.models import TransactionInterface

@dataclass
class TransactionResponse:
    response_code: int
    message: str
    transactions: list[TransactionInterface]