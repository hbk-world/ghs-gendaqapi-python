"""FieldBus Ring Buffer"""

from collections import deque
from .connection import ConnectionHandler

class FieldBusData:
    """FieldBus incoming packets, includes a timestamp and async values"""

    def __init__(self, dataCount):
        self.timeStamp = 0
        self.fValues = [0] * dataCount

class FieldBus:
    """Struct Definition for the FieldBus Connection"""

    conHandle = ConnectionHandler()
    ipAddress = None
    lastPacket = FieldBusData(0)

    def __init__(self, size, dataCount):
        self.dataHandle = FieldBusRingBuffer(size, dataCount)


class FieldBusRingBuffer:
    """FieldBus Ring Buffer Class"""

    def __init__(self, size, data_count):
        """Initialization of the FieldBus Ring Buffer Class"""

        self.buffer = [FieldBusData(data_count)] * size
        self.writeIndex = 0
        self.readIndex = 0
        self.capacity = size
        self.overrun = 0
        self.data_count = data_count

        self.ring_buffer_reset()

    def ring_buffer_reset(self):
        """Function to initialize some of the FieldBusRingBuf parameters"""

        self.buffer = [FieldBusData(self.data_count)] * self.capacity
        self.writeIndex = 0
        self.readIndex = 0
        self.overrun = 0

    def ring_buffer_free(self):
        """Destruction of the FieldBus Ring Buffer"""

        self.buffer = None

    def ring_buffer_is_empty(self):
        """Checks if the FieldBus Ring Buffer is empty"""

        return (not self.buffer and self.writeIndex == self.readIndex)

    def ring_buffer_get_size(self):
        """Retrieves the FieldBus Ring Buffer size"""

        if not self.buffer:
            print("Failed getting size of FieldBus Ring Buffer \n")
            return 0

        if self.writeIndex >= self.readIndex:
            size = self.writeIndex - self.readIndex
        else:
            size = self.capacity + self.writeIndex - self.readIndex

        return size

    def increment_writing_index(self):
        """Advances the Writing index"""

        if not self.buffer:
            print ("Failed accessing to the FieldBus Ring Buffer \n")
            return

        self.writeIndex = (self.writeIndex + 1) % self.capacity

        if self.writeIndex == self.readIndex:
            self.overrun = 1

    def increment_reading_index(self):
        """Advances the Writing index"""

        if not self.buffer:
            print ("Failed accessing to the FieldBus Ring Buffer \n")
            return

        self.readIndex = (self.readIndex + 1) % self.capacity

    def put_data(self, time_stamp, values):
        """Insert FieldBusData in the FieldBus Ring Buffer"""

        if not self.buffer:
            print("FieldBus Ring Buffer is null \n")
            return

        self.buffer[self.writeIndex].timeStamp = time_stamp
        self.buffer[self.writeIndex].fValues = values

        self.increment_writing_index()

    def get_data(self):
        """Read FieldBusData in the FieldBus Ring Buffer"""

        if not self.buffer:
            print("FieldBus Ring Buffer is null \n")
            return 0

        if not self.ring_buffer_is_empty():
            self.increment_reading_index()
            return (
                self.buffer[self.readIndex].timeStamp,
                self.buffer[self.readIndex].fValues,
                self.overrun
            )
