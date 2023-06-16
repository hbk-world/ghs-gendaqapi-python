# Copyright (C) 2022 Hottinger Bruel and Kjaer Benelux B.V.
# Schutweg 15a
# 5145 NP Waalwijk
# The Netherlands
# http://www.hbm.com

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Ring buffer class example.

This is to help you get started with Ring buffer class"""

import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src.ghsapi import fieldbus_ringbuffer


def main():
    """Code example to use ring buffer class"""

    ring_buffer = fieldbus_ringbuffer.FieldBusRingBuffer(5, 2)
    print(f"Ring buffer current size {ring_buffer.ring_buffer_size()}")
    print(
        f"Is ring buffer empty? {'no' if ring_buffer.ring_buffer_size() else 'yes'}"
    )
    ring_buffer.put_data(100, [1.1, 1.2])
    ring_buffer.put_data(101, [2.1, 2.2])
    ring_buffer.put_data(102, [3.1, 3.2])
    ring_buffer.put_data(103, [4.1, 4.2])
    ring_buffer.put_data(104, [5.1, 5.2])
    ring_buffer.put_data(104, [6.1, 6.2])
    print(f"Ring buffer current size {ring_buffer.ring_buffer_size()}")
    print(
        f"Is ring buffer empty? {'no' if ring_buffer.ring_buffer_size() else 'yes'}"
    )
    print(ring_buffer.get_data())
    print(ring_buffer.get_data())
    print(ring_buffer.get_data())
    print(ring_buffer.get_data())
    print(ring_buffer.get_data())
    print(ring_buffer.get_data())
    ring_buffer.ring_buffer_free()
    ring_buffer.put_data(102, [3.1, 3.2])


if __name__ == "__main__":
    main()
