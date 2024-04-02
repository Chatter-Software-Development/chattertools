import unittest
from datetime import datetime
from chattertools.helpers.parsers import parseDatetime

class TestParseDatetime(unittest.TestCase):

    def test_with_datetime(self):
        """Test with a datetime object."""
        input_val = datetime(2022, 1, 1, 0, 0)
        expected = input_val
        self.assertEqual(parseDatetime(input_val), expected)

    def test_with_unix_timestamp(self):
        """Test with a Unix timestamp."""
        input_val = 1640995200  # Equivalent to datetime(2022, 1, 1, 0, 0)
        expected = datetime.fromtimestamp(input_val)
        self.assertEqual(parseDatetime(input_val), expected)

    def test_with_correct_string(self):
        """Test with a correctly formatted string."""
        input_val = "2022-01-01T00:00:00.000Z"
        expected = datetime(2022, 1, 1, 0, 0)
        self.assertEqual(parseDatetime(input_val), expected)

    def test_with_incorrect_string(self):
        """Test with an incorrectly formatted string."""
        input_val = "not-a-valid-date"
        with self.assertRaises(ValueError):
            parseDatetime(input_val)

if __name__ == '__main__':
    unittest.main()
