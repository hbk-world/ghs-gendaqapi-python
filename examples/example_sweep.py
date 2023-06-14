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

    # Arm the trigger, so that the next trigger will be accepted
    return_var = gen.ghs_cmd_trigger_arm()
    if return_var != "OK":
        print(f"Failed on GHSCmdTriggerArm. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSCmdTriggerArm - Return Status: {return_var}"
    )

    # Determine the number of sweeps for a recorder
    return_var, number_sweeps = gen.ghs_get_number_of_sweeps("A")
    if return_var != "OK":
        print(f"Failed on GHSGetNumberOfSweeps. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetNumberOfSweeps - Return Status: {return_var}\
        Number Of Sweeps: {number_sweeps}"
    )

    # Determine the sweep length in samples for a recorder
    return_var, sweep_length = gen.ghs_get_sweep_length("A")
    if return_var != "OK":
        print(f"Failed on GHSGetSweepLength. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetSweepLength - Return Status: {return_var}\
        SweepLength: {sweep_length}"
    )

    # Determine the number of sweeps for a recorder
    return_var, sweep_mode = gen.ghs_get_sweep_recording_mode("A")
    if return_var != "OK":
        print(f"Failed on GHSGetSweepRecordingMode. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetSweepRecordingMode - Return Status: {return_var}\
        SweepMode: {sweep_mode}"
    )

    # Gets the sweep trigger mode for a recorder
    return_var, sweep_mode = gen.ghs_get_sweep_trigger_mode("A")
    if return_var != "OK":
        print(f"Failed on GHSGetSweepTriggerMode. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetSweepTriggerMode - Return Status: {return_var}\
        SweepTriggerMode: {sweep_mode}"
    )

    # Retrieve the timeout trigger enabled status
    return_var, enabled = gen.ghs_get_timeout_trigger_enabled()
    if return_var != "OK":
        print(f"Failed on GHSGetTimeoutTriggerEnabled. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetTimeoutTriggerEnabled - Return Status: {return_var}\
        Enabled: {enabled}"
    )

    # Retrieve the timeout trigger time
    return_var, time = gen.ghs_get_timeout_trigger_time()
    if return_var != "OK":
        print(f"Failed on GHSGetTimeoutTriggerTime. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetTimeoutTriggerTime - Return Status: {return_var}\
        Time: {time}"
    )

    # Retrieve trigger arm enabled status for a recorder
    return_var, enabled = gen.ghs_get_trigger_arm_enabled()
    if return_var != "OK":
        print(f"Failed on GHSGetTriggerArmEnabled. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetTriggerArmEnabled - Return Status: {return_var}\
        Enabled: {enabled}"
    )

    # Retrieve the current trigger arm state
    return_var, state = gen.ghs_get_trigger_arm_state()
    if return_var != "OK":
        print(f"Failed on GHSGetTriggerArmState. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetTriggerArmState - Return Status: {return_var}\
        TriggerArmState: {state}"
    )

    # Retrieve the timeout trigger time
    return_var, position = gen.ghs_get_trigger_position("A")
    if return_var != "OK":
        print(f"Failed on GHSGetTriggerPosition. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetTriggerPosition - Return Status: {return_var}\
        TriggerPosition: {position}"
    )

    # Sets the number of sweeps for a recorder
    return_var = gen.ghs_set_number_of_sweeps("A", 10)
    if return_var != "OK":
        print(f"Failed on GHSSetNumberOfSweeps. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetNumberOfSweeps - Return Status: {return_var}")

    # Sets the sweep length in samples for a recorder
    return_var = gen.ghs_set_sweep_length("A", 30)
    if return_var != "OK":
        print(f"Failed on GHSSetSweepLength. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetSweepLength - Return Status: {return_var}")

    # Sets the sweep recording mode for a recorder
    return_var = gen.ghs_set_sweep_recording_mode("A", "Normal")
    if return_var != "OK":
        print(f"Failed on GHSSetSweepRecordingMode. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetSweepRecordingMode - Return Status: {return_var}")

    # Sets the sweep trigger mode for a recorder
    return_var = gen.ghs_set_sweep_trigger_mode("A", "EveryTrigger")
    if return_var != "OK":
        print(f"Failed on GHSSetSweepTriggerMode. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetSweepTriggerMode - Return Status: {return_var}")

    # Enables or disables timeout triggers
    return_var = gen.ghs_set_timeout_trigger_enabled("Enable")
    if (return_var != "OK" and return_var != "Adapted"):
        print(f"Failed on GHSSetTimeoutTriggerEnabled. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetTimeoutTriggerEnabled - Return Status: {return_var}")

    # Sets the timeout trigger time
    return_var = gen.ghs_set_timeout_trigger_time(10.0)
    if (return_var != "OK" and return_var != "Adapted"):
        print(f"Failed on GHSSetTimeoutTriggerTime. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetTimeoutTriggerTime - Return Status: {return_var}")

    # Enable or disable trigger arm
    return_var = gen.ghs_set_trigger_arm_enabled("Enable")
    if (return_var != "OK" and return_var != "Adapted"):
        print(f"Failed on GHSSetTriggerArmEnabled. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetTriggerArmEnabled - Return Status: {return_var}")

    # Sets the trigger position percentage for a recorder
    return_var = gen.ghs_set_trigger_position("A", 50.0)
    if (return_var != "OK" and return_var != "Adapted"):
        print(f"Failed on GHSSetTriggerPosition. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetTriggerPosition - Return Status: {return_var}")

    # Disconnect
    return_var = gen.ghs_disconnect()
    if return_var != "OK":
        print(f"Failed on GHSDisconnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDisconnect - Return Status: {return_var}")


if __name__ == "__main__":
    main()
