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

"""The GEN DAQ Recorder API code examples.

This is to help you get started with Recorder API"""

import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src.ghsapi import ghsapi

IP_ADDRESS = "localhost"
PORT_NO = 8006


def main():
    """Code example to use Recorder API."""

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

    # Determine the continuous recording lead out time for a recorder
    return_var, lead_out_time = gen.ghs_get_continuous_lead_out_time("A")
    if return_var != "OK":
        print(f"Failed on GHSGetContinuousLeadOutTime. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetContinuousLeadOutTime - Return Status: {return_var}\
        ContinuousLeadOutTime: {lead_out_time}"
    )

    # Determine the continuous recording mode for a recorder
    return_var, mode = gen.ghs_get_continuous_recording_mode("A")
    if return_var != "OK":
        print(f"Failed on GHSGetContinuousRecordingMode. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetContinuousRecordingMode - Return Status: {return_var}\
        ContinuousRecordingMode: {mode}"
    )

    # Determine the continuous recording time span for a recorder
    return_var, time_span = gen.ghs_get_continuous_time_span("A")
    if return_var != "OK":
        print(f"Failed on GHSGetContinuousTimeSpan. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetContinuousTimeSpan - Return Status: {return_var}\
        ContinuousTimeSpan: {time_span}"
    )

    # Sets the continuous recording lead out time for a recorder
    return_var = gen.ghs_set_continuous_lead_out_time("A", 10.0)
    if return_var != "OK":
        print(f"Failed on GHSSetContinuousLeadOutTime. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetContinuousLeadOutTime - Return Status: {return_var}")

    # Set the continuous recording mode for a recorder
    return_var = gen.ghs_set_continuous_recording_mode("A", "Standard")
    if return_var != "OK":
        print(f"Failed on GHSSetContinuousRecordingMode. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetContinuousRecordingMode - Return Status: {return_var}")

    # Set the continuous recording time span for a recorder
    return_var = gen.ghs_set_continuous_time_span("A", 20.0)
    if return_var != "OK":
        print(f"Failed on GHSSetContinuousRecordingMode. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetContinuousRecordingMode - Return Status: {return_var}")

    # Disconnect
    return_var = gen.ghs_disconnect()
    if return_var != "OK":
        print(f"Failed on GHSDisconnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDisconnect - Return Status: {return_var}")


if __name__ == "__main__":
    main()
