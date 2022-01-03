"""The GEN DAQ Manage mainframe settings API code examples.

This is to help you get started with Manage mainframe settings API"""

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
    """Code example to use Manage mainframe settings API."""

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

    # Copy Active settings to Boot settings.
    return_var = gen.ghs_persist_current_settings()
    if return_var != "OK":
        print(
            f"Failed on GHSPersistCurrentSettings. Return Status: {return_var}"
        )
        sys.exit()
    print(f"GHSPersistCurrentSettings - Return Status: {return_var}")

    # Copy Boot settings to Active settings.
    return_var = gen.ghs_apply_persisted_settings()
    if return_var != "OK":
        print(
            f"Failed on GHSApplyPersistedSettings. Return Status: {return_var}"
        )
        sys.exit()
    print(f"GHSApplyPersistedSettings - Return Status: {return_var}")

    # Get GEN Mainframe settings.
    return_var, blob, blob_size = gen.ghs_get_current_settings()
    if return_var != "OK":
        print(f"Failed on GHSGetCurrentSettings. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetCurrentSettings - Return Status: {return_var}\
        Blob size: {blob_size}"
    )

    # Set  GEN Mainframe settings.
    return_var = gen.ghs_set_current_settings(blob, blob_size)
    if return_var != "OK":
        print(f"Failed on GHSSetCurrentSettings. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetCurrentSettings - Return Status: {return_var}")

    return_var = gen.ghs_disconnect()
    if return_var != "OK":
        print(f"Failed on GHSDisconnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDisconnect - Return Status: {return_var}")


if __name__ == "__main__":
    main()
