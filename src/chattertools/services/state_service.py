from typing import List
from ..models.transaction import Transaction
from .service import Service

from datetime import datetime

class StateService(Service):
    def __init__(self, requestor, machineId: int, *args, **kwargs):
        super().__init__(requestor, *args, **kwargs)
        
        self.machineId = machineId
    
    def get(self) -> List[Transaction]:
        """
        Get the state of a machine
        """
        data = self._requestor.get(f"/machines/{self.machineId}/state")
        return [Transaction.fromDict(d) for d in data]