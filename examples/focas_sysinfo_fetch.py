

import chattertools as ch

# Create the focas object and connect to the machine
focas = ch.Focas(
    ip='192.168.1.132', # IP of the machine     * Required
    port=8193,      # Port number           Default: 8193
    timeout=3       # Timeout in seconds    Default: 3
)
# class variables the store good information
print(focas._cncMethods) # stores the valid cnc methods for the current series
print(focas._controlSeries)# stores a string of the series of the machine ex "16ib"


# Get the cnc sys info 
response = focas.cnc_sysinfo()
print('Cnc additianl info:', "{0:b}".format(response.addinfo)) # return an int but need to convert to binaary to access individual bits 
print('Cnc Type', response.cnc_type)
print("Cnc Machine type", response.mt_type)
print('Cnc Number of Controlled axis:', response.axis)

# Disconnect from the machine
focas = None