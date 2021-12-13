"""The GEN DAQ Manage recordings API code examples.

This is to help you get started with Manage recordings API"""

import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src import ghsapi

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
        print(f"Failed on GHSGetStorageLocation. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetStorageLocation - Return Status: {return_var}\
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
