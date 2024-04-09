import ctypes


def focas_struct(cls):
    '''
    Decorator to make the ctypes _fileds_ signature easier to manipulate
    @focas_struct
    class foo(ctypes.structure):
        test: ctcypes.c_char * 255
        data: ctypes.c_short

    '''
    fields=[]
    for name, typ in cls.__annotations__.items():
        if isinstance(typ, tuple):
            s = typ
            fields.append((name, s[0], s[1]))
        else:
            fields.append((name, typ))
    cls._fields_ = fields
    return cls
