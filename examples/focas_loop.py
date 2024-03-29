import chattertools as ch
import time

focas = ch.Focas(ip='10.0.2.51')

while True:
    print('Macro 101', focas.cnc_rdmacro(101))
    print('Macro 102', focas.cnc_rdmacro(102))
    print('Macro 103', focas.cnc_rdmacro(103))
    
    time.sleep(2)

