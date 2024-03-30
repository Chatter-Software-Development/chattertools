from typing import List
from ..models.transaction import Transaction
from .service import Service

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
    
    def create(self, transaction: int) -> Transaction:
        raise NotImplementedError("Method not implemented")
        """
        Create a new transaction
        """
        data = transaction.toDict()
        data = self._requestor.post(f"/machines/{self.machineId}/transactions", data=data)
        return Transaction.fromDict(data)
    
    def delete(self, id: int) -> None:
        """
        Delete a transaction by ID
        """
        self._requestor.delete(f"/machines/{self.machineId}/transactions/{id}")
