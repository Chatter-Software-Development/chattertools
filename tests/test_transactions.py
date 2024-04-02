import unittest
import os
from dotenv import load_dotenv
import chattertools as ch
from chattertools.models import Transaction


class TestTransactions(unittest.TestCase):

    def test_create_valid_transactions(self):
        transactions = [
            Transaction(None, ch.DataType.MODE, 'MEM'),
            Transaction(None, ch.DataType.PART_COUNT, 100),
            Transaction(None, ch.DataType.ALARM_ACTIVE, True),
            Transaction(None, ch.DataType.ALARM_CONTENTS, 'Alarm Contents'),
            Transaction(None, ch.DataType.INSPECTION_SIZE, 1.23),
        ]
        self.assertTrue(len(transactions) > 0)