from datetime import datetime
from ..helpers.parsers import parseDatetime

class Transaction:
    def __init__(self, timestamp: datetime, dataType: str, value: str):
        self.timestamp = parseDatetime(timestamp)
        self.dataType = dataType
        self.value = value

    @staticmethod
    def fromDict(data: dict) -> 'Transaction':
        return Transaction(
            data['timestamp'],
            data['dataType'],
            data['value']
        )
    
    def toDict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "dataType": self.dataType,
            "value": self.value
        }
    
    def __str__(self):
        return f"Transaction {self.timestamp}: {self.dataType} - {self.value}"