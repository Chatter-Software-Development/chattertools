import chattertools as ch

# Create the focas object and connect to the machine
focas = ch.Focas(
    ip='10.0.2.51', # IP of the machine     * Required
    port=8193,      # Port number           Default: 8193
    timeout=3       # Timeout in seconds    Default: 3
)

MACRO_VAR = 101
NEW_VAL = 123.456

# Read the value of the macro variable
print(f'Macro {MACRO_VAR} value:', focas.cnc_rdmacro(MACRO_VAR))

# Set the value of the macro variable
focas.cnc_wrmacro(MACRO_VAR, NEW_VAL)

# Read the new value of the macro variable
print(f'Macro {MACRO_VAR} new value:', focas.cnc_rdmacro(MACRO_VAR))

# Disconnect from the machine
focas = None