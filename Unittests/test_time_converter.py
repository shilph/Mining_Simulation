import unittest

from time_converter import convert_sim_time_to_real_time_in_mil_sec, convert_unix_time_to_sim_timestamp


class TestTimeConversionFunctions(unittest.TestCase):
    def test_convert_sim_time_to_real_time_in_mil_sec(self):
        # General positive tests
        self.assertEqual(convert_sim_time_to_real_time_in_mil_sec(10, 1), 10000)
        self.assertEqual(convert_sim_time_to_real_time_in_mil_sec(0, 1), 0)
        self.assertEqual(convert_sim_time_to_real_time_in_mil_sec(1, 10), 100)
        self.assertEqual(convert_sim_time_to_real_time_in_mil_sec(10, 2), 5000)
        self.assertEqual(convert_sim_time_to_real_time_in_mil_sec(50, 5), 10000)

        # Check exceptions: sim_time_unit <= 0
        with self.assertRaises(ValueError):
            convert_sim_time_to_real_time_in_mil_sec(10, 0)
        with self.assertRaises(ValueError):
            convert_sim_time_to_real_time_in_mil_sec(10, -2)

    def test_convert_unix_time_to_sim_timestamp(self):
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

if __name__ == "__main__":
    unittest.main()
