import os
import platform
from pathlib import Path
from ctypes import *

from chattertools.focas_structs import *

class Focas:
    def __init__(self, ip: str, port: int = 8193, timeout: int = 3, logfile: str = 'focas.log'):
        self.config = {
            'ip': ip,
            'port': port,
            'timeout': timeout,
            'logfile': logfile
        }
        
        self.handle = c_ushort(0)

        self._loadDrivers()

        if self._isPlatformLinux():
            # Linux requires a logfile to exist while the connection is open, and a setup process to be run
            logfileName = self.config.get('logfile')
            self.fwlib.cnc_startupprocess(c_short(1), c_char_p(logfileName.encode('ascii')))

        self._getHandle()

    def __del__(self):
        if self.handle.value:
            self._releaseHandle()
        if self._isPlatformLinux():
            # Linux requires the exitprocess to be run when the connection is closed
            self.fwlib.cnc_exitprocess()

    def _getHandle(self):
        self.handle = self.cnc_allclibhndl3(self.config.get('ip'), self.config.get('port'), self.config.get('timeout'))

    def _releaseHandle(self):
        self.cnc_freelibhndl()

    # FOCAS Methods
    def cnc_allclibhndl3(self, ip: str, port: int, timeout: int = 10):
        """ Allocates the library handle and connects to CNC that has the specified IP address or the Host Name.
        Args:
            ip (str): The IP address of the CNC to connect to
            port (int): The port number to connect to
            timeout (int): The timeout for the connection
        Omitted Fanuc Args:
            handle: Pointer to the handle to be allocated
        Returns:
            int: The result of the connection
        """
        func = self.fwlib.cnc_allclibhndl3
        func.restype = c_short
        handle = c_ushort(0)
        result = func(ip.encode('ascii'), port, timeout, byref(handle))
        self._validateResponse(result)
        return handle
    
    def cnc_freelibhndl(self):
        """ Frees the library handle which was used by the Data window library.
        Args:
            None
        Omitted Fanuc Args:
            handle: Handle to be freed
        Returns:
            None
        """
        func = self.fwlib.cnc_freelibhndl
        func.restype = c_short
        result = func(self.handle)
        self._validateResponse(result)

    def cnc_exeprgname(self):
        """ Reads full path name of the program which is being currently executed in CNC.
            When the CNC is stopping, the name of the executed program is acquired.
            The program name is stored in "execprg.name" with maximum 32 character string format.
        Args:
            None
        Omitted Fanuc Args:
            handle: Handle to be freed
            exeprg: Structure to store the program name
        Returns:
            odbexeprg (class):
                name (str): The name of the program
                oNumber (int): The program number
        """
        f = self.fwlib.cnc_exeprgname
        f.argtypes = [c_ushort, POINTER(ODBEXEPRG)]
        f.restype = c_short

        exeprg = ODBEXEPRG()

        result = f(self.handle, byref(exeprg))
        self._validateResponse(result)

        return exeprg.getPyObj()
    
    def cnc_exeprgname2(self):
        """ Reads full path name of the program which is being currently executed in CNC.
            When the CNC is stopping, the name of the executed program is acquired.
            The program name is stored in "path_name" with maximum 256 character string format.
        Args: None
        Omitted Fanuc Args:
            handle
            char *path_name
        Returns:
            str: The full path of the program
        """
        f = self.fwlib.cnc_exeprgname2
        f.argtypes = [c_ushort, POINTER(c_char * 256)]
        f.restype = c_short

        path = (c_char * 256)()

        result = f(self.handle, byref(path))
        self._validateResponse(result)

        return path.value.decode('ascii').strip()
    
    def cnc_acts(self):
        """ Reads the actual rotational speed of the spindle connected to CNC.
            The actual spindle speed is stored in "data" of "ODBACT".
        Args:
            None
        Omitted Fanuc Args:
            handle: The handle
            odbact: Structure to store the spindle speed
        Returns:
            odbact (class):
                data (int): The actual spindle speed
        """
        f = self.fwlib.cnc_acts
        f.argtypes = [c_ushort, POINTER(ODBACT)]
        f.restype = c_short

        speed = ODBACT()

        result = f(self.handle, byref(speed))
        self._validateResponse(result)

        return speed.getPyObj()
    
    def cnc_statinfo(self):
        """ Reads the status information of CNC. The various information is stored in each member of "ODBST".
        
        Args:
            None
        Omitted Fanuc Args:
            handle: The handle
            ODBST: Structure to store the status information
        Returns:
            ODBST (class):
                aut (bool): AUTOMATIC mode selection
                manual (bool): MANUAL mode selection
                run (bool): Status of automatic operation
                edit (bool): Status of program editing
                motion (bool): Status of axis movement,dwell
                mstb (bool): Status of M,S,T,B function
                emergency (bool): Status of emergency
                write (bool): Status of writing backupped memory
                labelskip (bool): Status of label skip
                alarm (bool): Status of alarm
                warning (bool): Status of warning
                battery (bool): Status of battery
        """

        f = self.fwlib.cnc_statinfo
        f.argtypes = [c_ushort, POINTER(ODBST)]
        f.restype = c_short

        status = ODBST()

        result = f(self.handle, byref(status))
        self._validateResponse(result)

        return status.getPyObj()
    
    def cnc_rdalmmsg(self):
        f = self.fwlib.cnc_rdalmmsg
        f.argtypes = [c_ushort, c_short, POINTER(c_short), POINTER(ODBALMMSG)]
        f.restype = c_short

        quantity = c_short(10)
        buffer = ODBALMMSG()

        result = f(self.handle, c_short(-1), byref(quantity), byref(buffer))
        self._validateResponse(result)

        return buffer.getPyObj()
    
    def cnc_rdopmsg3(self):
        f = self.fwlib.cnc_rdopmsg3
        f.argtypes = [c_ushort, c_short, POINTER(c_short), POINTER(OPMSG)]
        f.restype = c_short

        sequenceNumber = c_short(-1)
        numberRead = c_short(5)
        buffer = OPMSG()
        ret = []

        result = f(self.handle, sequenceNumber, byref(numberRead), buffer)
        self._validateResponse(result)
        for x in range(int(numberRead.value)):
            if buffer.msg[x].datano != -1:
                msg = buffer.msg[x].data.decode('ascii').strip()
                ret.append(msg)
        

        return ret
    
    def cnc_rdmacro(self, number: int):
        f = self.fwlib.cnc_rdmacro
        f.argtypes = [c_ushort, c_short, c_short, POINTER(ODBM)]
        f.restype = c_short

        macro = ODBM()
        
        result = f(self.handle, c_short(number), c_short(12), byref(macro))
        self._validateResponse(result)

        return self.decodeFanucMacro(macro)
    
    def cnc_wrmacro(self, number: int, value: float):
        f = self.fwlib.cnc_wrmacro
        f.argtypes = [c_ushort, c_short, c_short, c_long, c_short]
        f.restype = c_short

        result = f(self.handle, c_short(number), c_short(10), *self.encodeFanucMacro(value))
        self._validateResponse(result)

        return True
    
    def cnc_sysinfo(self):
        """ Reads the system information of CNC. The various information is stored in each member of "ODBSYS".
        Args:
            None
        Omitted Fanuc Args:
            handle: The handle
            ODBSYS: Structure to store the system information
        Returns:
            odbsys(Class)
                addinfo (int)
                max_axis (int)
                cnc_type (str)
                mt_type (str)
                series (str)
                version (str)
                axes (str)
            """
        f = self.fwlib.cnc_sysinfo
        f.argtypes = [c_ushort,POINTER(ODBSYS)]
        f.restype = c_short

        _sys_info = ODBSYS()

        result = f(self.handle,byref(_sys_info))
        self._validateResponse(result)

        return _sys_info.getPyObj()

    @staticmethod
    def decodeFanucMacro(input: ODBM):
        macroVal = input.mcr_val
        decVal = input.dec_val

        if decVal in [-1, 65535]:
            return None # Vacant / Null variable in the control

        absValStr = f"{abs(macroVal):09d}"

        if 0 <= decVal <= 9:
            # Insert decimal point at the correct location
            valStr = absValStr[:9-decVal] + '.' + absValStr[9-decVal:]
        elif decVal > 9:
            # Insert decimal point at the start and then scale
            valStr = "." + absValStr
            value = float(valStr) / (10 ** (decVal - 9))
            if macroVal < 0:
                value = -value
            return value

        if macroVal < 0:
            valStr = "-" + valStr

        return float(valStr)
    
    @staticmethod
    def encodeFanucMacro(value: float):
        if value is None:
            # Handle null value
            return c_long(0), c_short(-1)

        # Convert the float to a string
        value_str = str(value)

        # Remove the decimal point and count how many places it moved
        if '.' in value_str:
            dot_index = value_str.index('.')
            value_str = value_str.replace('.', '')
            dec_val = dot_index
        else:
            dec_val = len(value_str)

        # Adjust the string length to 9 digits
        value_str = value_str[:9].ljust(9, '0')
        
        # Calculate mcr_val
        mcr_val = int(value_str)

        # Adjust dec_val to reflect the original decimal position
        dec_val = len(value_str) - dec_val

        return c_long(mcr_val), c_short(dec_val)

    def _loadDrivers(self):
        if self._isPlatformWindows():
            BASE_DIR = Path(__file__).resolve().parent
            DRIVER_DIR = os.path.join(BASE_DIR, 'lib', 'Fwlib64')
            DRIVER_NAME = 'Fwlib64'
            DRIVER_PATH = os.path.join(BASE_DIR, DRIVER_DIR, DRIVER_NAME + '.dll')

            if not os.path.exists(DRIVER_PATH):
                raise Exception(f"Driver not found at {DRIVER_PATH}")
            self.fwlib = windll.LoadLibrary(DRIVER_PATH)

            for file in os.listdir(DRIVER_DIR):
                if file.endswith('.dll'):
                    windll.LoadLibrary(os.path.join(DRIVER_DIR, file))

        elif self._isPlatformLinux():
            BASE_DIR = Path(__file__).resolve().parent
            DRIVER_DIR = './lib/'
            DRIVER_BASENAME = 'libfwlib32-linux'
            DRIVER_VERSION = '1.0.5'

            machine = platform.machine()
            if machine == 'armv7l':
                DRIVER_SUFFIX = '-armv7'
            elif machine == 'x86_64':
                DRIVER_SUFFIX = '-x64'
            elif machine == 'i386':
                DRIVER_SUFFIX = '-x86'
            else:
                raise Exception('Unsupported architecture: ' + machine)

            DRIVER_PATH = os.path.join(BASE_DIR, DRIVER_DIR, DRIVER_BASENAME + DRIVER_SUFFIX + '.so.' + DRIVER_VERSION)
            
            if not os.path.exists(DRIVER_PATH):
                raise Exception(f"Driver not found at {DRIVER_PATH}")
            self.fwlib = cdll.LoadLibrary(DRIVER_PATH)

        else:
            raise Exception('Unsupported platform: ' + platform.system())

    def _validateResponse(self, value):
        if value == 0 and value is not None:
            return
        errors = {
            -17: "Protocol Error (EW_PROTOCOL)",
            -16: "Socket error (EW_SOCKET)",
            -15: "DLL Not Found (EW_NODLL)",
            -11: "Bus error (EW_BUS)",
            -10: "System error (EW_SYSTEM2)",
            -9: "HSSB Serial error (EW_HSSB)",
            -8: "Handle error (EW_HANDLE)",
            -7: "CNC/PMC Version Mismatch (EW_VERSION)",
            -6: "Abnormal error??? (EW_UNEXP)",
            -5: "System error (EW_SYSTEM)",
            -4: "Shared RAM parity error (EW_PARITY)",
            -3: "EMM386 or mmcsys install error (EW_MMCSYS)",
            -2: "Reset or stop occurred (EW_RESET)",
            -1: "Busy error (EW_BUSY)",
            0: "No error (EW_OK)",
            1: "'Command prepare error (EW_FUNC)' or 'PMC does not exist (EW_NOPMC)'",
            2: "Data block length error (EW_LENGTH)",
            3: "Data number error (EW_NUMBER)",
            4: "'Data attribute error (EW_ATTRIB)' or 'Data type error (EW_TYPE)'",
            5: "Data error (EW_DATA)",
            6: "'No option' error (EW_NOOPT)",
            7: "Write protect error (EW_PROT)",
            8: "Memory overflow error (EW_OVRFLOW)",
            9: "CNC Parameter not correct (EW_PARAM)",
            10: "Buffer error (EW_BUFFER)",
            11: "Path error (EW_PATH)",
            12: "CNC Mode error (EW_MODE)",
            13: "Execution rejected (EW_REJECT)",
            14: "Data server error (EW_DTSRVR)",
            15: "Alarm occurred (EW_ALARM)",
            16: "CNC is not running (EW_STOP)",
            17: "Protection data error (EW_PASSWD)",
            18: "Error generated by PMC (EW_PMC)",
            19: "PMC Handle error (EW_PMCHANDLE)"
        }

        if value in errors:
            raise Exception(errors[value], value)
        else:
            message = f"An unknown value was provided to FocasException: {value}"
            raise Exception(message, value)

    @staticmethod
    def _isPlatformLinux():
        return platform.system() == 'Linux'
    
    @staticmethod
    def _isPlatformWindows():
        return platform.system() == 'Windows'