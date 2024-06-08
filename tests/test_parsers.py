import unittest
from datetime import datetime
from chattertools.helpers.parsers import Parse

class TestParsers(unittest.TestCase):
    def test_int(self):
        success = [
            ("1", 1),
            ("10", 10),
            ("21", 21),
        ]
        for x, expected in success:
            self.assertEqual(Parse.int(x).unwrap(), expected)

        failure = [
            "pizzeria",
            "21.1",
        ]
        for x in failure:
            self.assertTrue(Parse.int(x).err)

    def test_datetime(self):
        success = [
            # datetime object
            (datetime(2022, 1, 1, 0, 0), datetime(2022, 1, 1, 0, 0)),
            # Unix timestamp
            (1640995200, datetime(2021, 12, 31, 18, 0)),
            # Supported string format
            ("2022-01-01T00:00:00.000Z", datetime(2022, 1, 1, 0, 0)),
        ]
        for x, expected in success:
            self.assertEqual(Parse.datetime(x).unwrap(), expected)

        failure = [
            "not-a-valid-date",
            "pizzeria",
        ]
        for x in failure:
            self.assertTrue(Parse.datetime(x).err)

    def test_bool(self):
        success = [
            # None
            (None, None),
            # bool
            (True, True),
            (False, False),
            # int
            (0, False),
            (1, True),
            # string
            ("true", True),
            ("false", False),
            # NOTE: These should probably be an error :P
            ("", False), 
            ("potato", False), 
        ]
        for x, expected in success:
            self.assertEqual(Parse.bool(x).unwrap(), expected)

        failure = [
            2,
            10,
        ]
        for x in failure:
            self.assertTrue(Parse.datetime(x).err)

if __name__ == '__main__':
    unittest.main()
