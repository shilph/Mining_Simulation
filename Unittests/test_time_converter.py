import unittest

from time_converter import (
    convert_sim_time_to_real_time_in_sec,
    convert_unix_time_to_sim_timestamp,
)


class TestTimeConversionFunctions(unittest.TestCase):
    """Unit tests for time_converter."""

    def test_convert_sim_time_to_real_time_in_sec(self):
        """Test convert_sim_time_to_real_time_in_sec"""

        # General positive tests
        self.assertEqual(convert_sim_time_to_real_time_in_sec(10, 1), 10)
        self.assertEqual(convert_sim_time_to_real_time_in_sec(0, 1), 0)
        self.assertEqual(convert_sim_time_to_real_time_in_sec(1, 10), 0.1)
        self.assertEqual(convert_sim_time_to_real_time_in_sec(10, 2), 5)
        self.assertEqual(convert_sim_time_to_real_time_in_sec(50, 5), 10)

        # Check exceptions: sim_time_unit <= 0
        with self.assertRaises(ValueError):
            convert_sim_time_to_real_time_in_sec(10, 0)
        with self.assertRaises(ValueError):
            convert_sim_time_to_real_time_in_sec(10, -2)

    def test_convert_unix_time_to_sim_timestamp(self):
        """Test convert_unix_time_to_sim_timestamp"""

        # General positive tests
        self.assertEqual(convert_unix_time_to_sim_timestamp(1000.0, 1000.0, 1), "00:00")
        self.assertEqual(convert_unix_time_to_sim_timestamp(1000.0, 1060.0, 1), "01:00")
        self.assertEqual(convert_unix_time_to_sim_timestamp(1000.0, 1090.0, 1), "01:30")
        self.assertEqual(convert_unix_time_to_sim_timestamp(1000.0, 1030.0, 2), "01:00")
        self.assertEqual(convert_unix_time_to_sim_timestamp(1000.0, 1090.0, 5), "07:30")

        # Check exceptions: sim_time_unit <= 0
        with self.assertRaises(ValueError):
            convert_unix_time_to_sim_timestamp(1000.0, 1050.0, 0)
        with self.assertRaises(ValueError):
            convert_unix_time_to_sim_timestamp(1000.0, 1050.0, -1)
        # Check exceptions: curr_unix_time < unix_time_start
        with self.assertRaises(ValueError):
            convert_unix_time_to_sim_timestamp(100.0, 50.0, 1)
