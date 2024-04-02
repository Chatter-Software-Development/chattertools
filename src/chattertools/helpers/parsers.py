from datetime import datetime
from typing import Any, Union

def parseInt(val: Any) -> int:
    if val is None: return None
    try:
        return int(val)
    except ValueError:
        raise ValueError(f"Cannot convert value {val} to integer")

def parseDatetime(val: Union[datetime, int, str]) -> datetime:
    if val is None: return None

    if isinstance(val, datetime): return val
    if isinstance(val, int): return datetime.fromtimestamp(val)

    if isinstance(val, str):
        formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S"]
        for format in formats:
            try:
                return datetime.strptime(val, format)
            except ValueError:
                pass

        raise ValueError(f'Invalid datetime format "{val}"')
    
def parseApiDatetime(val: datetime) -> str:
    return val.strftime("%Y-%m-%d %H:%M:%S")
    
def parseBool(val: Union[bool, int, str]) -> bool:
    if val is None: return None
    if isinstance(val, bool): return val
    if isinstance(val, int):
        try:
            return bool(val)
        except ValueError:
            pass
    if isinstance(val, str): return val.lower() == "true"
    raise ValueError(f"Cannot convert value {val} to boolean")