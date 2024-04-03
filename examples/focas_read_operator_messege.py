import chattertools as ch

# Create the focas object and connect to the machine
focas = ch.Focas(
    ip='192.168.1.132', # IP of the machine     * Required
    port=8193,      # Port number           Default: 8193
    timeout=3       # Timeout in seconds    Default: 3
)

# get the operator messages 
response = focas.cnc_rdopmsg3()
print(response)