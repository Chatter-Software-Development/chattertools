from datetime import datetime
from typing import Any, Union
from result import Result, Ok, Err

class Parse:
    @staticmethod
    def int(val: Any) -> Result[int, str]:
        if val is None: return None
        try:
            return Ok(int(val))
        except ValueError:
            return Err(f"Cannot convert value {val} to integer")

    @staticmethod
    def datetime(val: Union[datetime, int, str]) -> Result[datetime, str]:
        if val is None: return Ok(None)

        if isinstance(val, datetime): return Ok(val)
        if isinstance(val, int): return Ok(datetime.fromtimestamp(val))

        if isinstance(val, str):
            formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S"]
            for format in formats:
                try:
                    return Ok(datetime.strptime(val, format))
                except ValueError:
                    pass

            return Err(f'Invalid datetime format "{val}"')
    
    @staticmethod
    def apiDatetime(val: datetime) -> Result[str, str]:
        try:
            return Ok(val.strftime("%Y-%m-%d %H:%M:%S"))
        except Exception:
            return Err(f"Failed to format \"{val}\" as a valid datetime string")
    
    @staticmethod
    def bool(val: Union[bool, int, str]) -> bool:
        if val is None: return Ok(None)
        if isinstance(val, bool): return Ok(val)
        if isinstance(val, int):
            try:
                return Ok(bool(val))
            except ValueError:
                return Err(f"Failed to coerce integer to bool \"{val}\"")
        if isinstance(val, str): return Ok(val.lower() == "true")
        return Err(f"Cannot convert value {val} to boolean")