from typing import List

from .macro import Macro
from ..services.macro_service import MacroService
from .transaction import Transaction
from ..services.transaction_service import TransactionService

class Machine:
    def __init__(self, requestor, id: int, name: str):
        self._requestor = requestor
        self.id = id
        self.name = name

        self._macros = None
        self._transactions = None

    @property
    def macros(self) -> List[Macro]:
        if self._macros is None:
            self._macros = MacroService(self._requestor, self.id)
        return self._macros
    
    @property
    def transactions(self) -> List[Transaction]:
        if self._transactions is None:
            self._transactions = TransactionService(self._requestor, self.id)
        return self._transactions

    @classmethod
    def fromDict(cls, requestor, data: dict) -> 'Machine':
        return cls(requestor, data['id'], data['name'])
    
    def toDict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }
    
    def __str__(self):
        return f"Machine {self.id}: {self.name}"