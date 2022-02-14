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

"""The GEN DAQ Channel API code examples.

This is to help you get started with Channel API"""

import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src.ghsapi import ghsapi

IP_ADDRESS = "localhost"
PORT_NO = 8006


def main():
    """Code example to use Channel API."""

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

    # Set channel name
    return_var = gen.ghs_set_channel_name("A", 1, "NewChannelName")
    if return_var != "OK":
        print(f"Failed on GHSSetChannelName. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetChannelName - Return Status: {return_var}")

    # Get channel name
    return_var, channel_name = gen.ghs_get_channel_name("A", 1)
    if return_var != "OK":
        print(f"Failed on GHSGetChannelName. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetChannelName - Return Status: {return_var}\
        Channel name: {channel_name}"
    )

    # Enable or disable storage for a channel
    return_var = gen.ghs_set_channel_storage_enabled("A", 1, "Enable")
    if return_var != "OK":
        print(
            f"Failed on GHSSetChannelStorageEnabled. Return Status: {return_var}"
        )
        sys.exit()
    print(f"GHSSetChannelStorageEnabled - Return Status: {return_var}")

    # Determine if storage is enabled or disabled for a channel
    return_var, enabled = gen.ghs_get_channel_storage_enabled("A", 1)
    if return_var != "OK":
        print(
            f"Failed on GHSGetChannelStorageEnabled. Return Status: {return_var}"
        )
        sys.exit()
    print(
        f"GHSGetChannelStorageEnabled - Return Status: {return_var}\
        Channel enabled: {enabled}"
    )

    # Get channel type
    return_var, channel_type = gen.ghs_get_channel_type("A", 1)
    if return_var != "OK":
        print(f"Failed on GHSGetChannelType. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetChannelType - Return Status: {return_var}\
        Channel type: {channel_type}"
    )

    # Perform zeroing in a channel
    return_var = gen.ghs_cmd_zeroing("A", 1, "Enable")
    if return_var != "OK":
        print(f"Failed on GHSCmdZeroing. Return Status: {return_var}")
        sys.exit()
    print(f"GHSCmdZeroing - Return Status: {return_var}")

    # Disconnect
    return_var = gen.ghs_disconnect()
    if return_var != "OK":
        print(f"Failed on GHSDisconnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDisconnect - Return Status: {return_var}")


if __name__ == "__main__":
    main()
