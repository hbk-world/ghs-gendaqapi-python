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

"""The GEN DAQ Connections API example.

This is to help you get started with Connections API"""

import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src.ghsapi import ghsapi

IP_ADDRESS = "localhost"
PORT_NO = 8006


def main():
    """Code example to use connections API."""

    gen = ghsapi.GHS()

    return_var = gen.ghs_connect(IP_ADDRESS, PORT_NO)

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
