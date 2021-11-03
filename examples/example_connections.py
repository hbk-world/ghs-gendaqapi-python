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
    print("GHSConnect: ", return_var)

    return_var = gen.ghs_get_current_access()
    print("Client access: ", return_var)

    return_var = gen.ghs_disconnect()
    print("GHSDisconnect: ", return_var)


if __name__ == "__main__":
    main()
