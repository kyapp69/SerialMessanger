import unittest
import sys
import os
from mock import Mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from serial_messanger import SerialMessanger


class SerialMessangerTest(unittest.TestCase):
    def call_back(*args):
        pass

    def setUp(self):
        self.test_serial_messanger = None
        self.mock_connection = Mock()
        self.test_serial_messanger = SerialMessanger(self.mock_connection, handshake=None)

    def tearDown(self):
        if self.test_serial_messanger:
            if self.test_serial_messanger.is_alive():
                self.test_serial_messanger.close()
                self.test_serial_messanger.join(1)

    def test_starts_and_stops(self):
        self.test_serial_messanger.start()
        self.assertEquals(True, self.test_serial_messanger.is_alive())
        self.test_serial_messanger.close()
        self.assertEquals(False, self.test_serial_messanger.is_alive())
        self.test_serial_messanger.join(1)

    def test_start_flushes_connection(self):
        self.test_serial_messanger.start()
        self.test_serial_messanger.close()
        self.test_serial_messanger.join(1)
        self.mock_connection.flushInput.assert_called_with()
        self.mock_connection.flushOutput.assert_called_with()

    def test_start_should_transmit_handshake_if_provided_and_wait_for_a_response(self):
        expected_header = 'aaa'
        expected_footer = 'ccc'
        expected_handshake = 'hello'
        send_bytes = expected_header + expected_handshake + expected_footer
        return_bytes = list(send_bytes)

        def side_effect(self):
            if bytes:
                return return_bytes.pop(0)
            else:
                raise Exception('test failure read too many bytes')
        self.mock_connection.read.side_effect = side_effect
        self.test_serial_messanger = SerialMessanger(self.mock_connection, header=expected_header, footer=expected_footer, handshake=expected_handshake)
        self.test_serial_messanger.start()
        self.test_serial_messanger.close()
        self.test_serial_messanger.join(1)
        self.mock_connection.write.assert_called_with(send_bytes)

    def test_never_recieves_handshake(self):
        expected_header = 'aaa'
        expected_footer = 'ccc'
        expected_handshake = 'hello'
        self.mock_connection.read.return_value = 'z'
        self.test_serial_messanger = SerialMessanger(self.mock_connection, header=expected_header, footer=expected_footer, handshake=expected_handshake, handshake_timeout_sec=0.3)
        with self.assertRaises(Exception):
            self.test_serial_messanger.start()
        self.assertFalse(self.test_serial_messanger.is_alive())

    def test_register_id_must_be_between_0_and_255(self):
        with self.assertRaises(Exception):
            self.test_serial_messanger.register(-1, self.call_back, 'h')
        with self.assertRaises(Exception):
            self.test_serial_messanger.register(256, self.call_back, 'h')

        self.test_serial_messanger.register(1, self.call_back, 'h')

    def test_register_types_must_be_struct_compatible(self):
        with self.assertRaises(Exception):
            self.test_serial_messanger.register(1, self.call_back, 'a')
        with self.assertRaises(Exception):
            self.test_serial_messanger.register(1, self.call_back, type(123))
        self.test_serial_messanger.register(1, self.call_back, 'b')

if __name__ == '__main__':
    unittest.main()
