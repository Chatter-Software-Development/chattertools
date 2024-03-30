import unittest
import os
from dotenv import load_dotenv
from chattertools import ChatterClient

class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.client = ChatterClient(os.getenv('CHATTER_API_KEY'))

    def test_machine_list(self):
        machines = self.client.machine.list()
        print('List machines')
        for m in machines: print(m)
        self.assertTrue(len(machines) > 0)

    def test_machine_get(self):
        machines = self.client.machine.list()
        self.assertTrue(len(machines) > 0)
        machine = self.client.machine.get(machines[0].id)
        print('Get machine')
        print(machine)
        self.assertEqual(machine.id, machines[0].id)

    def test_machine_transaction_list(self):
        machines = self.client.machine.list()
        self.assertTrue(len(machines) > 0)
        transactions = machines[0].transactions.list()
        print('List transactions')
        for t in transactions: print(t)
        self.assertTrue(len(transactions) > 0)

    def test_machine_macro_list(self):
        machines = self.client.machine.list()
        self.assertTrue(len(machines) > 0)
        macros = machines[0].macros.list()
        print('List macros')
        for m in macros: print(m)
        self.assertTrue(len(macros) > 0)

    def test_machine_macro_get(self):
        machines = self.client.machine.list()
        self.assertTrue(len(machines) > 0)
        macros = machines[0].macros.list()
        self.assertTrue(len(macros) > 0)
        macro = machines[0].macros.get(macros[0].id)
        print('Get macro')
        print(macro)
        self.assertEqual(macro.id, macros[0].id)