from typing import List
from ..models.macro import Macro
from .service import Service

class MacroService(Service):
    def __init__(self, requestor, machineId: int, *args, **kwargs):
        super().__init__(requestor, *args, **kwargs)
        
        self.machineId = machineId

    def list(self, limit: int = 100, offset: int = 0) -> List[Macro]:
        """
        List all macros
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        data = self._requestor.get(f"/machines/{self.machineId}/macros", params=params)
        return [Macro.fromDict(macro) for macro in data]
    
    def get(self, id: int) -> Macro:
        raise NotImplementedError("Method not implemented")
        """
        Get a macro by ID
        """
        data = self._requestor.get(f"/machines/{id}/macros/{id}")
        return Macro.fromDict(data)
    
    def create(self, macroVariable: int) -> Macro:
        raise NotImplementedError("Method not implemented")
        """
        Create a new macro
        """
        data = macroVariable.toDict()
        data = self._requestor.post(f"/machines/{self.machineId}/macros", data=data)
        return Macro.fromDict(data)
    
    def delete(self, id: int) -> None:
        """
        Delete a macro by ID
        """
        self._requestor.delete(f"/machines/{self.machineId}/macros/{id}")
