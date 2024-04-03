

import chattertools as ch

# Create the focas object and connect to the machine
focas = ch.Focas(
    ip='192.168.1.132', # IP of the machine     * Required
    port=8193,      # Port number           Default: 8193
    timeout=3       # Timeout in seconds    Default: 3
)

# Get the program name
response = focas.cnc_sysinfo()
print('Cnc additianl info:', response.addinfo)
print('Cnc Series', response.series)
print('Cnc Max axis:', response.max_axis)

# Disconnect from the machine
focas = None