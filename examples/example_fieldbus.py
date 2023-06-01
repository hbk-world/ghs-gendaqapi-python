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

"""The GEN DAQ Fieldbus API code examples.

This is to help you get started with Fieldbus API"""

import os
import sys
import time

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src.ghsapi import ghsapi

IP_ADDRESS = "10.96.129.154"
PORT_NO = 8006


def main():
    """Code example to use Fieldbus API."""

    gen = ghsapi.GHS()

    # Connect to the mainframe "localhost" is also possible.
    return_var = gen.ghs_connect(IP_ADDRESS, PORT_NO)
    if return_var == "APIMismatch":
        print("Failed on GHSConnect. Client API version mismatch")
        sys.exit()
    if return_var != "OK":
        print(f"Failed on GHSConnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSConnect - Return Status: {return_var}")

    # Start preview mode (this enables EtherCAT output).
    return_var = gen.ghs_start_preview()
    if return_var != "OK":
        print(f"Failed on GHSStartPreview. Return Status: {return_var}")
        sys.exit()
    print(f"GHSStartPreview - Return Status: {return_var}")
    time.sleep(1)

    # Do something while the GHS mainframe is in preview mode
    return_var, data_count = gen.ghs_get_fieldbus_data_count()
    if return_var != "OK":
        print(f"Failed on GHSGetFieldBusDataCount. Return Status: {return_var}")
        sys.exit()
    print(f"GHSGetFieldBusDataCount - Return Status: {return_var} Data Count: {data_count}")

    dict_published = {}
    # Get the data name and unit for each data index. The data index starts from 1.
    for data_index in range(0, data_count or 0):
        return_var, data_name, data_unit = gen.ghs_get_fieldbus_data_name_and_unit(data_index)
        dict_published[data_name] = data_unit
        if return_var != "OK":
            print(f"Failed on GHSGetFieldBusDataNameAndUnit. Return Status: {return_var}")
            sys.exit()
        print(f"GHSGetFieldBusDataNameAndUnit - Return Status: {return_var} Data Unit: {data_unit} Data Name: {data_name}")

    for iterations in range(0, 10):
        return_var, timestamp, data_count, data = gen.ghs_get_fieldbus_request_snapshot(data_count or 0)
        if return_var != "OK":
            print(f"Failed on GHSRequestFieldBusData. Return Status: {return_var}")
            sys.exit()
        print(f"GHSRequestFieldBusData - Return Status: {return_var} Timestamp: {timestamp}")
        index: int = 0
        for fieldbus_data in dict_published:
            print(f"    Data Name: {fieldbus_data} Data Value: {data[index] or 0} {dict_published[fieldbus_data]}")
            index = index + 1

        time.sleep(1)

    return_var = gen.ghs_stop_preview()
    if return_var != "OK":
        print(f"Failed on GHSStopPreview. Return Status: {return_var}")
        sys.exit()
    print(f"GHSStopPreview - Return Status: {return_var}")

    # Disconnect to the mainframe "localhost" is also possible.
    return_var = gen.ghs_disconnect()
    if return_var != "OK":
        print(f"Failed on GHSDisconnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDisconnect - Return Status: {return_var}")


if __name__ == "__main__":
    main()
