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

"""The GEN DAQ Manage recordings API code examples.

This is to help you get started with Manage recordings API"""

import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src.ghsapi import ghsapi

IP_ADDRESS = "localhost"
PORT_NO = 8006


def main():
    """Code example to use Manage recordings API."""

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

    # Set the storage location
    return_var = gen.ghs_set_storage_location("Local1")
    if return_var != "OK":
        print(f"Failed on GHSSetStorageLocation. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetStorageLocation - Return Status: {return_var}")

    # Get the storage location
    return_var, storage_location = gen.ghs_get_storage_location()
    if return_var != "OK":
        print(f"Failed on GHSGetStorageLocation. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetStorageLocation - Return Status: {return_var}\
        Storage Location: {storage_location}"
    )

    # Set the recoding name and index
    return_var = gen.ghs_set_recording_name("Test1", 2)
    if return_var != "OK":
        print(f"Failed on GHSSetRecordingName. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetRecordingName - Return Status: {return_var}")

    # Get the recoding name and index
    return_var, recording_name, recording_index = gen.ghs_get_recording_name()
    if return_var != "OK":
        print(f"Failed on GHSGetRecordingName. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetRecordingName - Return Status: {return_var}\
        Recording name: {recording_name}\
        Recording index: {recording_index}"
    )

    # Delete last recoding
    return_var = gen.ghs_delete_last_recording()
    if return_var != "OK":
        print(f"Failed on GHSDeleteLastRecording. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDeleteLastRecording - Return Status: {return_var}")

    # Delete all recodings
    return_var = gen.ghs_delete_all_recordings()
    if return_var != "OK":
        print(f"Failed on GHSDeleteAllRecordings. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDeleteAllRecordings - Return Status: {return_var}")

    # Set high low rate storage
    return_var = gen.ghs_set_high_low_rate_storage_enabled(
        "SyncChannels", "A", "Enable", "Enable"
    )
    if return_var != "OK":
        print(
            f"Failed on GHSSetHighLowRateStorageEnabled. Return Status: {return_var}"
        )
        sys.exit()
    print(f"GHSSetHighLowRateStorageEnabled - Return Status: {return_var}")

    # Get high low rate storage
    return_var, high, low = gen.ghs_get_high_low_rate_storage_enabled(
        "SyncChannels", "A"
    )
    if return_var != "OK":
        print(
            f"Failed on GHSGetHighLowRateStorageEnabled. Return Status: {return_var}"
        )
        sys.exit()
    print(
        f"GHSGetHighLowRateStorageEnabled - Return Status: {return_var}\
        High rate: {high}\
        Low rate: {low}"
    )

    return_var = gen.ghs_disconnect()
    if return_var != "OK":
        print(f"Failed on GHSDisconnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDisconnect - Return Status: {return_var}")


if __name__ == "__main__":
    main()
