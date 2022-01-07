"""The GEN DAQ Recorder API code examples.

This is to help you get started with Recorder API"""

import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src import ghsapi

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

    # Get recorder information
    return_var, rec_type, name, serial, version = gen.ghs_get_recorder_info(
        "A"
    )
    if return_var != "OK":
        print(
            f"Failed on GHSGetRecorderInformation. Return Status: {return_var}"
        )
        sys.exit()
    print(
        f"GHSGetRecorderInformation - Return Status: {return_var}\
        \nRecorder Type : {rec_type}\
        Recorder Name: {name}\
        Serial Number: {serial}\
        Firmware version: {version}"
    )

    # Get channel count
    return_var, channel_count = gen.ghs_get_channel_count("A")
    if return_var != "OK":
        print(f"Failed on GHSGetChannelCount. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetChannelCount - Return Status: {return_var}\
        Channel count: {channel_count}"
    )

    # Set sample rate
    return_var = gen.ghs_set_sample_rate("A", 1000.0)
    if return_var != "OK":
        print(f"Failed on GHSSetSampleRate. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetSampleRate - Return Status: {return_var}")

    # Get sample rate
    return_var, sample_rate = gen.ghs_get_sample_rate("A")
    if return_var != "OK":
        print(f"Failed on GHSGetSampleRate. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetSampleRate - Return Status: {return_var}\
        Sample rate: {sample_rate}"
    )

    # Set output digital mode
    return_var = gen.ghs_set_digital_output("A", "Output1", "High")
    if return_var != "OK":
        print(f"Failed on GHSSetDigitalOutput. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetDigitalOutput - Return Status: {return_var}")

    # Get output digital mode
    return_var, digital_mode = gen.ghs_get_digital_output("A", "Output1")
    if return_var != "OK":
        print(f"Failed on GHSGetDigitalOutput. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetDigitalOutput - Return Status: {return_var}\
        Digital output mode: {digital_mode}"
    )

    # Set recorder enabled
    return_var = gen.ghs_set_recorder_enabled("A", "Disable")
    if return_var != "OK":
        print(f"Failed on GHSSetRecorderEnabled. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetRecorderEnabled - Return Status: {return_var}")

    # Get recorder enabled
    return_var, enabled = gen.ghs_get_recorder_enabled("A")
    if return_var != "OK":
        print(f"Failed on GHSGetRecorderEnabled. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetRecorderEnabled - Return Status: {return_var}\
        Recorder enabled: {enabled}"
    )

    return_var = gen.ghs_disconnect()
    if return_var != "OK":
        print(f"Failed on GHSDisconnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDisconnect - Return Status: {return_var}")


if __name__ == "__main__":
    main()
