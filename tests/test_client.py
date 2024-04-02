import unittest
import os
from dotenv import load_dotenv
import chattertools as ch
from chattertools.models import Transaction

class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.client = ch.Client(os.getenv('CHATTER_API_KEY'))

    def test_machine_list(self):
        machines = self.client.machines.list()
        self.assertTrue(len(machines) > 0)

    def test_machine_get(self):
        machines = self.client.machines.list()
        self.assertTrue(len(machines) > 0)
        machine = self.client.machines.get(machines[0].id)
        self.assertEqual(machine.id, machines[0].id)

    def test_machine_transaction_list(self):
        machines = self.client.machines.list()
        self.assertTrue(len(machines) > 0)
        transactions = machines[0].transactions.list()
        for t in transactions: print(t)
        self.assertTrue(len(transactions) > 0)

    def test_machine_transaction_create(self):
        machines = self.client.machines.list()
        self.assertTrue(len(machines) > 0)
        transaction = machines[0].transactions.create(None, ch.DataType.TOOL , 5)
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.dataType, ch.DataType.TOOL)
        self.assertEqual(transaction.value, 5)

    def test_machine_state_get(self):
        machines = self.client.machines.list()
        self.assertTrue(len(machines) > 0)
        state = machines[0].state.get()
        self.assertTrue(len(state) > 0)
        for s in state: print(s)