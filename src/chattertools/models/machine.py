from typing import List

from .macro import Macro
from ..services.macro_service import MacroService
from .transaction import Transaction
from ..services.transaction_service import TransactionService
from ..services.state_service import StateService
from .transaction import Transaction

class Machine:
    def __init__(self, requestor, id: int, name: str):
        self._requestor = requestor
        self.id = id
        self.name = name

        self._state = None
        self._transactions = None
        self._macros = None

    @property
    def state(self) -> List[Transaction]:
        if self._state is None:
            self._state = StateService(self._requestor, self.id)
        return self._state
    
    @property
    def transactions(self) -> List[Transaction]:
        if self._transactions is None:
            self._transactions = TransactionService(self._requestor, self.id)
        return self._transactions

    @property
    def macros(self) -> List[Macro]:
        if self._macros is None:
            self._macros = MacroService(self._requestor, self.id)
        return self._macros

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