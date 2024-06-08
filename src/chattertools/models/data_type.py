from enum import Enum
from datetime import datetime
from ..helpers.parsers import Parse

class DataType(Enum):
    MODE = (1, str)
    PROGRAM = (2, str)
    PART_COUNT = (3, int)
    PART_GOAL = (4, int)
    PALLET = (5, str)
    ALARM_ACTIVE = (6, bool)
    ALARM_CONTENTS = (7, str)
    MESSAGE_ACTIVE = (8, bool)
    MESSAGE_CONTENTS = (9, str)
    TOOL = (10, int)
    TAKT_TIME = (11, int)
    COMPLETION_TIME = (12, datetime)
    Q500 = (13, str)
    STATUS = (14, str)
    SPINDLE_SPEED = (21, int)
    COOLANT_LEVEL = (22, float)
    AIR_PRESSURE = (23, float)
    IN_CYCLE_TIME = (24, int)
    TOOL_TIMER = (25, int)
    INSPECTION_SIZE = (26, float)
    INSPECTION_TOLERANCE = (27, float)
    INSPECTION_SIZE_ERROR = (28, float)
    CUSTOM_DATA_1 = (29, str)
    CUSTOM_DATA_2 = (30, str)
    CUSTOM_DATA_3 = (31, str)
    IN_CYCLE = (32, bool)
    ONLINE = (33, bool)
    RAW_DEBUG = (34, str)
    PROGRAM_ID = (35, int)
    INSPECTION_X_POSITION = (36, float)
    INSPECTION_X_ERROR = (37, float)
    INSPECTION_Y_POSITION = (38, float)
    INSPECTION_Y_ERROR = (39, float)
    INSPECTION_Z_POSITION = (40, float)
    INSPECTION_Z_ERROR = (41, float)
    INSPECTION_FEATURE_ID = (42, float)
    INSPECTION_TRUE_POSITION_ERROR = (43, float)

    def __init__(self, value, type):
        self._value_ = value
        self.type = type

    @classmethod
    def fromValue(cls, value):
        for dt in cls:
            if dt._value_ == value:
                return dt
        raise ValueError(f"Unknown data type: {value}")
    
    @staticmethod
    def getParser(type):
        if type == int:
            return Parse.int
        if type == bool:
            return Parse.bool
        if type == float:
            return float
        if type == datetime:
            return Parse.datetime
        if type == str:
            return str
        return None