import ctypes
from typing import List, Tuple, Type, TypeVar, Union

StructType = TypeVar("StructType", bound=[ctypes.Structure])

def focus_struct(cls: StructType) -> StructType:
    '''
    Decorator to make the ctypes _fileds_ signature easier to manipulate
    @focus_struct
    class foo(ctypes.structure):
        test: ctcypes.c_char * 255
        data: ctypes.c_short

    '''
    fields: List[Union[Tuple[str, type],Tuple[str, type, int]]]=[]
    for name, typ in cls.__annotations__.items():
        if isinstance(typ, tuple):
            s : Tuple[type, int] = typ
            fields.append((name, s[0], s[1]))
        else:
            fields.append((name, typ))
    cls._fields_ = fields
    return cls
