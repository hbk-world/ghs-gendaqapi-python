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

"""The GEN DAQ FieldBus API code examples.

This is to help you get started with FieldBus API"""

import os
import sys
import time

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src.ghsapi import ghsapi

IP_ADDRESS = "localhost"
PORT_NO = 8006


def main():
    """Code example to use FieldBus API."""

    update_rate = 1
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

    # Open a new connection for the field bus data
    (
        return_var,
        update_rate,
        data_count,
    ) = gen.ghs_initiate_fieldbus_data_transfer(update_rate)
    if return_var != "OK":
        print(
            f"Failed on GHSInitiateFieldBusDataTransfer. Return Status: {return_var}"
        )
        sys.exit()
    print(
        f"GHSInitiateFieldBusDataTransfer - Return Status: {return_var}\
        \nUpdate rate : {update_rate}\
        Data count: {data_count}"
    )

    # Closes the socket dedicated for the field bus data and stops transfering data.
    return_var = gen.ghs_stop_fieldbus_data_transfer()
    if return_var != "OK":
        print(
            f"Failed on GHSStopFieldBusDataTransfer. Return Status: {return_var}"
        )
        sys.exit()
    print(f"GHSStopFieldBusDataTransfer - Return Status: {return_var}")

    # Gets the number of data that are configured to be sent through the field bus
    return_var, data_count = gen.ghs_get_fieldbus_data_count()
    if return_var != "OK":
        print(
            f"Failed on GHSGetFieldBusDataCount. Return Status: {return_var}"
        )
        sys.exit()
    print(
        f"GHSGetFieldBusDataCount - Return Status: {return_var}\
        \nData count: {data_count}"
    )

    # Gets the name of specific field bus data value, by giving the index of the data value
    for data_index in range(data_count):

        (
            return_var,
            data_name,
            data_unit,
        ) = gen.ghs_get_fieldbus_data_name_and_unit(data_index)
        if return_var != "OK":
            print(
                f"Failed on GHSGetFieldBusDataNameAndUnit for index {data_index + 1}. Return Status: {return_var}"
            )
            sys.exit()
        print(
            f"GHSGetFieldBusDataNameAndUnit - Return Status: {return_var}\
            \nData index : {data_index}\
            \nData name : {data_name}\
            Data unit: {data_unit}"
        )

    # Start preview mode
    return_var = gen.ghs_start_preview()
    if return_var != "OK":
        print(f"Failed on GHSStartPreview. Return Status: {return_var}")
        sys.exit()
    print(f"GHSStartPreview - Return Status: {return_var}")
    time.sleep(1)

    # Request a single snapshot of the field bus data.
    (
        return_var,
        time_stamp,
        data_count,
        data,
    ) = gen.ghs_request_fieldbus_snapshot()
    if return_var != "OK":
        print(
            f"Failed on GHSRequestFieldBusSnapshot. Return Status: {return_var}"
        )
        sys.exit()
    print(
        f"GHSRequestFieldBusSnapshot - Return Status: {return_var}\
        \nTimestamp : {time_stamp}\
        \nData count : {data_count}\
        Data: {data}"
    )

    # Stop preview mode
    return_var = gen.ghs_stop_preview()
    if return_var != "OK":
        print(f"Failed on GHSStopPreview. Return Status: {return_var}")
        sys.exit()
    print(f"GHSStopPreview - Return Status: {return_var}")

    return_var = gen.ghs_disconnect()
    if return_var != "OK":
        print(f"Failed on GHSDisconnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDisconnect - Return Status: {return_var}")


if __name__ == "__main__":
    main()
