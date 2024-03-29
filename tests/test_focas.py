import unittest
from chattertools import Focas
import os

class TestFocas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.focas = Focas(ip='10.0.2.51', port=8193, timeout=3)

    def test_cnc_allclibhndl3(self):
        self.assertTrue(self.focas.handle != 0)

    def test_cnc_exeprgname(self):
        response = self.focas.cnc_exeprgname()
        print('cnc_exeprgname', response)
        self.assertTrue(response != None)

    def test_acts(self):
        response = self.focas.cnc_acts()
        print('cnc_acts', response)
        self.assertTrue(response != None)

    def test_cnc_statinfo(self):
        response = self.focas.cnc_statinfo()
        print('cnc_statinfo', response)
        self.assertTrue(response != None)

    def test_cnc_rdalmmsg(self):
        response = self.focas.cnc_rdalmmsg()
        print('cnc_rdalmmsg', response)
        self.assertTrue(response != None)

    def test_rdopmsg3(self):
        response = self.focas.cnc_rdopmsg3()
        print('cnc_rdopmsg3', response)
        self.assertTrue(response != None)

    def test_cnc_rdmacro(self):
        MACRO_VAR = 101
        response = self.focas.cnc_rdmacro(MACRO_VAR)
        print('cnc_rdmacro', response)
        self.assertTrue(response != None)

    def test_cnc_wrmacro(self):
        MACRO_VAR = 102
        TEST_VALUE = 1234.5678
        self.focas.cnc_wrmacro(MACRO_VAR, TEST_VALUE)
        macroRead = self.focas.cnc_rdmacro(MACRO_VAR)
        print('cnc_wrmacro', macroRead, '==' if ( macroRead == TEST_VALUE) else '!=', TEST_VALUE)
        self.assertTrue(macroRead == TEST_VALUE)

    @classmethod
    def tearDownClass(self):
        self.focas = None
        if os.path.exists('focas.log'):
            os.remove('focas.log')

if __name__ == '__main__':
    unittest.main()