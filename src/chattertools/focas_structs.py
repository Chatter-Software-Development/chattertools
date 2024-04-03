
import ctypes

class ODBM(ctypes.Structure):
    _fields_ =[
        ('datano', ctypes.c_short),
        ('dummy', ctypes.c_short),
        ('mcr_val', ctypes.c_long),
        ('dec_val', ctypes.c_long)
    ]


class ODBEXEPRG(ctypes.Structure):
    _pack_ = 4
    _fields_ = [("name", ctypes.c_char * 36),
                ("oNumber", ctypes.c_long), ]
    
    def getPyObj(self):
        return odbexeprg(self.name, self.oNumber)
    
class odbexeprg():
    def __init__(self, name, oNumber):
        self.name = name.decode('ascii').strip()
        self.oNumber = int(oNumber)

    def __str__(self):
        return f'obdexeprg(name={self.name}, oNumber={self.oNumber})'


class ODBST(ctypes.Structure):
    _fields_ = [
        ('dummy', ctypes.c_short * 2),
        ('aut', ctypes.c_short),
        ('manual', ctypes.c_short),
        ('run', ctypes.c_short),
        ('edit', ctypes.c_short),
        ('motion', ctypes.c_short),
        ('mstb', ctypes.c_short),
        ('emergency', ctypes.c_short),
        ('write', ctypes.c_short),
        ('labelskip', ctypes.c_short),
        ('alarm', ctypes.c_short),
        ('warning', ctypes.c_short),
        ('battery', ctypes.c_short),
    ]

    def getPyObj(self):
        return odbst(self.aut, self.manual, self.run, self.edit, self.motion, self.mstb, self.emergency, self.alarm, self.write, self.labelskip, self.warning, self.battery)
    
class odbst():
    def __init__(self, aut, manual, run, edit, motion, mstb, emergency, alarm, write, labelskip, warning, battery):
        self.aut = self._getMapping('aut', aut)
        self.manual = self._getMapping('manual', manual)
        self.run = self._getMapping('run', run)
        self.edit = self._getMapping('edit', edit)
        self.motion = self._getMapping('motion', motion)
        self.mstb = self._getMapping('mstb', mstb)
        self.emergency = self._getMapping('emergency', emergency)
        self.alarm = self._getMapping('alarm', alarm)
        self.write = self._getMapping('write', write)
        self.labelskip = self._getMapping('labelskip', labelskip)
        self.warning = self._getMapping('warning', warning)
        self.battery = self._getMapping('battery', battery)

    def _getMapping(self, key, value):
        mappings = {
            'aut': [None, 'MDI', 'DNC', 'MEM', 'EDIT', 'TH IN'],
            'manual': [None, 'REF', 'INC', 'HND', 'JOG', 'AGJ', 'I+H', 'J+H'],
            'run': ['STOP', 'HOLD', 'STRT', 'MSTR', 'RSTR', 'PRSR', 'NSRC', 'RSTR', 'RSET', None, None, None, None, 'HPCC'],
            'edit': [None, 'EDIT', 'SRCH', 'VRFY', 'COND', 'READ', 'PNCH'],
            'motion': [None, 'MTN', 'DWL', 'W'],
            'mstb': [None, 'FIN'],
            'emergency': [False, True],
            'write': [False, True],
            'labelskip': [True, False],
            'alarm': [False, True],
            'warning': [False, True],
            'battery': [False, True, True]
        }

        if (key in mappings):
            if (value < len(mappings[key])):
                return mappings[key][value]
            else:
                raise ValueError(f'No mapping found for key {key} at value {value}')
        else:
            raise ValueError(f'No mapping found for {key}')

    def __str__(self):
        return f'odbst(aut={self.aut}, manual={self.manual}, run={self.run}, edit={self.edit}, motion={self.motion}, mstb={self.mstb}, emergency={self.emergency}, alarm={self.alarm}, write={self.write}, labelskip={self.labelskip}, warning={self.warning}, battery={self.battery})'

class ODBACT(ctypes.Structure):
    _fields_ = [
        ('dummy', ctypes.c_short * 2),
        ('data', ctypes.c_long)
    ]

    def getPyObj(self):
        return odbact(self.data)

class odbact():
    def __init__(self, data):
        self.data = int(data)

    def __str__(self):
        return f'odbact(data={self.data})'

class OPMSG(ctypes.Structure):
    _fields_ = [
        ('datano', ctypes.c_short),
        ('type', ctypes.c_short),
        ('char_num', ctypes.c_short),
        ('data', ctypes.c_char * 256)
    ]

class ODBALMMSG(ctypes.Structure):
    _fields_ = [
        ("alm_no", ctypes.c_long),
        ("type", ctypes.c_short),
        ("axis", ctypes.c_short),
        ("dummy", ctypes.c_short),
        ("msg_len", ctypes.c_short),
        ("alm_msg", ctypes.c_char * 32)
    ]

    def getPyObj(self):
        return odbalmmsg(self.alm_no, self.type, self.axis, self.msg_len, self.alm_msg)

class odbalmmsg():
    def __init__(self, alm_no, type, axis, msg_len, alm_msg):
        self.alm_no = int(alm_no)
        self.type = int(type)
        self.axis = int(axis)
        self.msg_len = int(msg_len)
        self.alm_msg = alm_msg.decode('ascii').strip()

    def __str__(self):
        return f'odbalmmsg(alm_no={self.alm_no}, type={self.type}, axis={self.axis}, msg_len={self.msg_len}, alm_msg={self.alm_msg})'
    
class ODBSYS(ctypes.Structure):
    '''Used with cnc_sysinfo  MS'''
    _fields_ = [
        ('addinfo',ctypes.c_short),
        ('max_axis', ctypes.c_short),
        ('cnc_type', ctypes.c_char * 2),
        ('mt_type', ctypes.c_char * 2),
        ('series', ctypes.c_char * 4),
        ('version', ctypes.c_char * 4),
        ('axis', ctypes.c_char * 2)
    ]

    def getPyObj(self):
        return odbsys(self.addinfo, self.max_axis, self.cnc_type, self.mt_type, self.series, self.version, self.axis)
    
class odbsys():
    def __init__(self, addinfo, max_axis, cnc_type, mt_type, series, version, axis):
            self.addinfo = int(addinfo)
            self.max_axis = int(max_axis)
            self.cnc_type = cnc_type.decode('ascii').strip()
            self.mt_type = mt_type.decode('ascii').strip()
            self.series = series.decode('ascii').strip()
            self.version = version.decode('ascii').strip()
            self.axis = axis.decode('ascii').strip() #prefer to conver to int but expected return is string
    
    def __str__(self) -> str:
        return f'odbsys(addinfo={self.addinfo}, max_axis={self.max_axis}, cnc_type={self.cnc_type}, mt_type={self.mt_type}, series={self.series}, version={self.version}, axis={self.axis})'
    