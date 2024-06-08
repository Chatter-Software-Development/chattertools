from datetime import datetime
from ..helpers.parsers import Parse
from .data_type import DataType
from typing import Any

class Transaction:
    def __init__(self, timestamp: datetime, dataType: DataType, value: Any):
        self.timestamp = Parse.datetime(timestamp) if timestamp else datetime.now()
        self.dataType = dataType
        self.value = self.enforceType(dataType, value)

    @staticmethod
    def fromDict(data: dict) -> 'Transaction':
        return Transaction(
            data['timestamp'],
            DataType.fromValue(int(data['dataType'])),
            str(data['value'])
        )
    
    def toDict(self) -> dict:
        return {
            "timestamp": Parse.apiDatetime(self.timestamp),
            "dataType": self.dataType.value,
            "value": str(self.value)
        }
    
    @staticmethod
    def enforceType(dataType: DataType, value):
        if value is None:
            return None
        parser = DataType.getParser(dataType.type)
        value = parser(value).unwrap() if parser else value
        if not isinstance(value, dataType.type):
            raise TypeError(f"Value {value} is not of type {dataType.type}, got {type(value)} instead")
        return value
    
    def __str__(self):
        return f"Transaction {self.timestamp}: {self.dataType} - {self.value}"