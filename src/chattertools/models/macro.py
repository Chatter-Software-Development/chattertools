class Macro:
    def __init__(self, id: int, macroVariable: int):
        self.id = id
        self.macroVariable = macroVariable

    @staticmethod
    def fromDict(data: dict) -> 'Macro':
        return Macro(data['id'], data['macroVariable'])
    
    def toDict(self) -> dict:
        return {
            "id": self.id,
            "macroVariable": self.macroVariable
        }
    
    def __str__(self):
        return f"Macro {self.id}: {self.macroVariable}"