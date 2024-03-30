from datetime import datetime

def parseInt(val: str) -> int:
    if val is None: return None
    return int(val)

def parseDatetime(val: str):
    if val is None: return None
    format = "%Y-%m-%dT%H:%M:%S.%fZ"
    return datetime.strptime(val, format)