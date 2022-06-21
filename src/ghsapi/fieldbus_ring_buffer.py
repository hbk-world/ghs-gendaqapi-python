"""FieldBus Ring Buffer"""

from collections import deque


class FieldBusData:
    """FieldBus incoming packets, includes a timestamp and async values"""

    def __init__(self) -> None:
        self.time_stamp = None
        self.values = []


class RingBuffer:
    """FieldBus Ring Buffer"""

    def __init__(self):
        self.buffer = None
        self.capacity = None
        self.overrun = None
        self.data_count = None


class FieldBusRingBuffer:
    """FieldBus Ring Buffer Class"""

    def __init__(self, size, data_count):
        """Initialization of the FieldBus Ring Buffer Class"""

        self.ring_buffer = RingBuffer()
        self.ring_buffer.capacity = size
        self.ring_buffer.data_count = data_count

        self.ring_buffer_reset()

    def ring_buffer_reset(self):
        """Function to initialize some of the FieldBusRingBuf parameters"""

        self.ring_buffer.buffer = deque(maxlen=self.ring_buffer.capacity)
        self.ring_buffer.overrun = 0

    def ring_buffer_free(self):
        """Destruction of the FieldBus Ring Buffer"""

        self.ring_buffer = None

    def ring_buffer_empty(self):
        """Checks if the FieldBus Ring Buffer is empty"""

        return not self.ring_buffer.buffer

    def ring_buffer_size(self):
        """Retrieves the FieldBus Ring Buffer size"""

        return len(self.ring_buffer.buffer)

    def put_data(self, time_stamp, values):
        """Insert FieldBusData in the FieldBus Ring Buffer"""

        if not self.ring_buffer:
            print("FieldBus Ring Buffer is null \n")
            return

        if self.ring_buffer_size() >= self.ring_buffer.capacity:
            self.ring_buffer.overrun = 1

        data = FieldBusData()
        data.time_stamp = time_stamp
        data.values = values

        self.ring_buffer.buffer.append(data)

    def get_data(self):
        """Read FieldBusData in the FieldBus Ring Buffer"""

        if not self.ring_buffer:
            print("FieldBus Ring Buffer is null \n")
            return 0

        if not self.ring_buffer_empty():
            data = self.ring_buffer.buffer.popleft()

            return data.time_stamp, data.values, self.ring_buffer.overrun
