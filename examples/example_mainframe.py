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

"""The GEN DAQ Mainframe API code examples.

This is to help you get started with Mainframe API"""

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
    """Code example to use Mainframe API."""

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

    # Get total and free disk size.
    return_var, total, available = gen.ghs_get_disk_space()
    if return_var != "OK":
        print(f"Failed on GHSGetDiskSpace. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetDiskSpace - Return Status: {return_var}\
        Total disk space: {total}\
        Available disk space: {available}"
    )

    # Get slot count.
    return_var, slot_count = gen.ghs_get_slot_count()
    if return_var != "OK":
        print(f"Failed on GHSGetSlotCount. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetSlotCount - Return Status: {return_var}\
        Slot count: {slot_count}"
    )

    # Get synchronization status.
    return_var, sync_status = gen.ghs_get_sync_status()
    if return_var != "OK":
        print(f"Failed on GHSGetSyncStatus. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetSyncStatus - Return Status: {return_var}\
        Sync status: {sync_status}"
    )

    # Get user mode.
    return_var, user_mode = gen.ghs_get_user_mode()
    if return_var != "OK":
        print(f"Failed on GHSGetUserMode. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetUserMode - Return Status: {return_var}\
        User mode: {user_mode}"
    )

    # Set user mode.
    return_var = gen.ghs_set_user_mode("Continuous")
    if return_var != "OK":
        print(f"Failed on GHSSetUserMode. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetUserMode - Return Status: {return_var}")

    # Get mainframe info.
    return_var, main_type, name, serial, version = gen.ghs_get_mainframe_info()
    if return_var != "OK":
        print(
            f"Failed on GHSGetMainframeInformation. Return Status: {return_var}"
        )
        sys.exit()
    print(
        f"GHSGetMainframeInformation - Return Status: {return_var}\
        \nMainframe type : {main_type}\
        Mainframe name: {name}\
        Serial no.: {serial}\
        Firmware version: {version}"
    )

    # Enable & diable identify
    return_var = gen.ghs_identify(True)
    if return_var != "OK":
        print(f"Failed on GHSIdentify Enable. Return Status: {return_var}")
        sys.exit()
    print(f"GHSIdentify Enable - Return Status: {return_var}")
    time.sleep(2)
    return_var = gen.ghs_identify(False)
    if return_var != "OK":
        print(f"Failed on GHSIdentify Disable. Return Status: {return_var}")
        sys.exit()
    print(f"GHSIdentify Disable - Return Status: {return_var}")

    return_var = gen.ghs_disconnect()
    if return_var != "OK":
        print(f"Failed on GHSDisconnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDisconnect - Return Status: {return_var}")


if __name__ == "__main__":
    main()
