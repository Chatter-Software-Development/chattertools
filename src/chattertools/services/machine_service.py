from typing import List
from ..models.machine import Machine
from .service import Service

class MachineService(Service):
    def __init__(self, requestor, *args, **kwargs):
        super().__init__(requestor, *args, **kwargs)

    def list(self, limit: int = 100, offset: int = 0) -> List[Machine]:
        """
        List all machines
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        data = self._requestor.get("/machines", params=params)
        return [Machine.fromDict(self._requestor, machine) for machine in data]
    
    def get(self, id: int) -> Machine:
        """
        Get a machine by ID
        """
        data = self._requestor.get(f"/machines/{id}")
        return Machine.fromDict(self._requestor, data)