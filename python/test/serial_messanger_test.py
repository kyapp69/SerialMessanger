import unittest
import sys
import os
from mock import patch, Mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from serial_messanger import SerialMessanger


class SerialMessangerTest(unittest.TestCase):
    def call_back(*args):
        pass

    def setUp(self):
        self.test_serial_messanger = None

    def tearDown(self):
        if self.test_serial_messanger:
            if self.test_serial_messanger.is_alive():
                self.test_serial_messanger.close()
                self.test_serial_messanger.join(1000)

    def test_register_id_must_be_between_0_and_255(self):
        mock_connection = Mock()
        self.test_serial_messanger = SerialMessanger(mock_connection)
        with self.assertRaises(Exception):
            self.test_serial_messanger.register(-1, self.call_back, type(123))
        with self.assertRaises(Exception):
            self.test_serial_messanger.register(256, self.call_back, type(123))

        self.test_serial_messanger.register(1, self.call_back, type(123))

    def test_starts_and_stops(self ):
        mock_connection = Mock()
        self.test_serial_messanger = SerialMessanger(mock_connection)
        self.test_serial_messanger.start()
        self.assertEquals(True, self.test_serial_messanger.is_alive())
        self.test_serial_messanger.close()
        self.assertEquals(False, self.test_serial_messanger.is_alive())
        self.test_serial_messanger.join(1000)

    def test_start_flushes_connection(self):
        mock_connection = Mock()
        self.test_serial_messanger = SerialMessanger(mock_connection)
        self.test_serial_messanger.start()
        self.test_serial_messanger.close()
        self.test_serial_messanger.join(1000)
        mock_connection.flushInput.assert_called_with()
        mock_connection.flushOutput.assert_called_with()


if __name__ == '__main__':
    unittest.main()