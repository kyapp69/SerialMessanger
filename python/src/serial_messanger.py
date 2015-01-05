import struct
import threading
import time


'''Tool for serial communication alling for registration and call back of methods based on input data
Usage:
'''


class SerialMessanger(threading.Thread):
    '''Initialize the class with a started connection matching the pyserialAPI (http://pyserial.sourceforge.net/pyserial_api.html)
    Note: You will need to manage the starting and stopping of this connection outside of this class'''
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    '''Registers a handler and arg types for a specific message id.
    message_id - Message ids should be an integer between 0 and 255 (inclusive)
    callback   - Method taking the types as parameters
    types      - A list of ordered types corrosponding to the callback parameters'''
    def register(self, message_id, callback, types):
        self._is_valid_id(message_id)

    def _is_valid_id(self, message_id):
        if message_id < 0 or message_id > 255:
            raise Exception('Message Id must be a integer between 0 and 255 (inclusive)')

    def run(self):
        self._running = True
        self.connection.flushInput()
        self.connection.flushOutput()
        while(self._running):
            pass

    def close(self):
        self._running = False
        while self.is_alive():
            time.sleep(0.1)
