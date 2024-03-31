from typing import List
from ..models.transaction import Transaction
from .service import Service

from datetime import datetime

class TransactionService(Service):
    def __init__(self, requestor, machineId: int, *args, **kwargs):
        super().__init__(requestor, *args, **kwargs)
        
        self.machineId = machineId

    def list(self, limit: int = 100, offset: int = 0) -> List[Transaction]:
        """
        List all transactions
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        data = self._requestor.get(f"/machines/{self.machineId}/transactions", params=params)
        return [Transaction.fromDict(t) for t in data]
    
    def get(self, id: int) -> Transaction:
        raise NotImplementedError("Method not implemented")
        """
        Get a transaction by ID
        """
        data = self._requestor.get(f"/machines/{id}/transactions/{id}")
        return Transaction.fromDict(data)
    
    def create(self, timestamp: datetime, dataType: int, value: str) -> Transaction:
        """
        Create a new transaction
        """
        transaction = Transaction(timestamp, dataType, value)
        data = self._requestor.post(f"/machines/{self.machineId}/transactions", data=transaction.toDict())
        return Transaction.fromDict(data)