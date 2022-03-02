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

    # Set trigger setting for analog channel
    return_var = gen.ghs_set_trigger_settings(
        "A", 1, "Dual", 10, 20, 30, "RisingEdge"
    )
    if (return_var != "OK") and (return_var != "Adapted"):
        print(f"Failed on GHSSetTriggerSettings. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetTriggerSettings - Return Status: {return_var}")

    # Get trigger setting for analog channel
    (
        return_var,
        trigger_mode,
        primary_level,
        secondary_level,
        hysteresis,
        direction,
    ) = gen.ghs_get_trigger_settings("A", 1)
    if return_var != "OK":
        print(f"Failed on GHSGetTriggerSettings. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetTriggerSettings - Return Status: {return_var}\
        Trigger Mode: {trigger_mode}\
        Primary Level: {primary_level}\
        Secondary Level: {secondary_level}\
        Hysteresis: {hysteresis}\
        Direction: {direction}"
    )

    # Set the signal coupling for an analog channel.
    return_var = gen.ghs_set_signal_coupling("A", 1, "DC")
    if return_var != "OK" and return_var != "Adapted":
        print(f"Failed on GHSSetSignalCoupling. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetSignalCoupling - Return Status: {return_var}")

    # Determine the signal coupling for an analog channel.
    return_var, signal_coupling = gen.ghs_get_signal_coupling("A", 1)
    if return_var != "OK":
        print(f"Failed on GHSGetSignalCoupling. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetSignalCoupling - Return Status: {return_var}\
        Signal Coupling: {signal_coupling}"
    )

    # Set the input coupling for an analog channel.
    return_var = gen.ghs_set_input_coupling("A", 1, "Current")
    if return_var != "OK" and return_var != "Adapted":
        print(f"Failed on GHSSetInputCoupling. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetInputCoupling - Return Status: {return_var}")

    # Determine the input coupling for an analog channel.
    return_var, input_coupling = gen.ghs_get_input_coupling("A", 1)
    if return_var != "OK":
        print(f"Failed on GHSGetInputCoupling. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetInputCoupling - Return Status: {return_var}\
        Input Coupling: {input_coupling}"
    )

    # Set Span and offset for analog channels.
    return_var = gen.ghs_set_span_and_offset("A", 1, 10.0, 20.0)
    if return_var != "OK" and return_var != "Adapted":
        print(f"Failed on GHSSetSpanAndOffset. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetSpanAndOffset - Return Status: {return_var}")

    # Determine the span and offset for an analog channel.
    return_var, span, offset = gen.ghs_get_span_and_offset("A", 1)
    if return_var != "OK":
        print(f"Failed on GHSGetSpanAndOffset. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetSpanAndOffset - Return Status: {return_var}\
        Span: {span}\
        Offset: {offset}"
    )

    # Set the filter type and frequency for an analog channel.
    return_var = gen.ghs_set_filter_type_and_frequency(
        "A", 1, "Bessel_AA", 150000.0
    )
    if return_var != "OK" and return_var != "Adapted":
        print(
            f"Failed on GHSSetFilterTypeAndFrequency. Return Status: {return_var}"
        )
        sys.exit()
    print(f"GHSSetFilterTypeAndFrequency - Return Status: {return_var}")

    # Determine the filter type and frequency for an analog channel.
    return_var, filter_type, frequency = gen.ghs_get_filter_type_and_frequency(
        "A", 1
    )
    if return_var != "OK":
        print(
            f"Failed on GHSGetFilterTypeAndFrequency. Return Status: {return_var}"
        )
        sys.exit()
    print(
        f"GHSGetFilterTypeAndFrequency - Return Status: {return_var}\
        Filter Type: {filter_type}\
        Frequency: {frequency}"
    )

    # Disconnect
    return_var = gen.ghs_disconnect()
    if return_var != "OK":
        print(f"Failed on GHSDisconnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDisconnect - Return Status: {return_var}")


if __name__ == "__main__":
    main()
