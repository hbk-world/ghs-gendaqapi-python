"""The GEN DAQ Acquisition API code examples.

This is to help you get started with Acquisition API"""

import os
import sys
import time

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src import ghsapi

IP_ADDRESS = "localhost"
PORT_NO = 8006


def main():
    """Code example to use Acquisition API."""

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

    return_var, year, day, sec = gen.ghs_get_acquisition_start_time()
    print(
        f"GHSGetAcquisitionStartTime - Year:{year} Days:{day} Secs:{sec}\
        Return Status: {return_var}"
    )

    # Do something while the GHS mainframe is in preview mode
    # (e.g. monitor output data on EtherCAT).

    return_var = gen.ghs_stop_preview()
    if return_var != "OK":
        print(f"Failed on GHSStopPreview. Return Status: {return_var}")
        sys.exit()
    print(f"GHSStopPreview - Return Status: {return_var}")

    # Start recording.
    # Note: the mainframe should be configured to store recordings
    # on its local disk.
    return_var = gen.ghs_start_recording()
    if return_var != "OK":
        print(f"Failed on GHSStartRecording. Return Status: {return_var}")
        sys.exit()
    print(f"GHSStartRecording - Return Status: {return_var}")

    # Do something while the GHS mainframe is recording
    return_var, acquisition_state = gen.ghs_get_acquisition_state()
    print(
        f"GHSGetAcquisitionState: {acquisition_state}\
             Return Status: {return_var}"
    )

    return_var, acq_time = gen.ghs_get_acquisition_time()
    print(
        f"GHSGetAcquisitionTime: {acq_time}\
        Return Status: {return_var}"
    )

    # Pause recording.
    return_var = gen.ghs_pause_recording()
    if return_var != "OK":
        print(f"Failed on GHSPauseRecording. Return Status: {return_var}")
        sys.exit()
    print(f"GHSPauseRecording - Return Status: {return_var}")
    time.sleep(1)

    # Resume recording
    return_var = gen.ghs_resume_recording()
    if return_var != "OK":
        print(f"Failed on GHSResumeRecording. Return Status: {return_var}")
        sys.exit()
    print(f"GHSResumeRecording - Return Status: {return_var}")

    # Trigger
    return_var = gen.ghs_trigger()
    if return_var != "OK":
        print(f"Failed on GHSTrigger. Return Status: {return_var}")
        sys.exit()
    print(f"GHSTrigger - Return Status: {return_var}")

    # Stop recording
    return_var = gen.ghs_stop_recording()
    if return_var != "OK":
        print(f"Failed on GHSStopRecording. Return Status: {return_var}")
        sys.exit()
    print(f"GHSStopRecording - Return Status: {return_var}")

    return_var = gen.ghs_disconnect()
    if return_var != "OK":
        print(f"Failed on GHSDisconnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDisconnect - Return Status: {return_var}")


if __name__ == "__main__":
    main()
