"""The GEN DAQ API code examples.

This is to help you get started"""

import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src import ghsapi


def main():
    """Code example to use connections API."""

    gen = ghsapi.GHS()

    return_var = gen.ghs_connect("localhost", 8006)

    if return_var == "APIMismatch":
        print("Failed on GHSConnect: Client API version mismatch")
        sys.exit()
    if return_var != "OK":
        print(f"Failed on GHSConnect: return status is {return_var}")
        sys.exit()

    print("GHSConnect: ", return_var)

    return_var = gen.ghs_get_client_api_version()
    print("Client API version: ", return_var)

    return_var = gen.ghs_get_current_access()
    print("Client access: ", return_var)

    return_var = gen.ghs_disconnect()

    if return_var != "OK":
        print(f"Failed on GHSDisconnect: return status is {return_var}")
        sys.exit()

    print("GHSDisconnect: ", return_var)


if __name__ == "__main__":
    main()
