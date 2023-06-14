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

IP_ADDRESS = "10.96.130.163"
PORT_NO = 8006


def main():
    """Code example to use Formulas API."""

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

    # Get number of scalar formulas in the Mainframe.
    return_var, number_scalars = gen.ghs_get_number_of_scalars()
    if return_var != "OK":
        print(f"Failed on GHSGetNumberOfScalars. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetNumberOfScalars - Return Status: {return_var}\
        Number Of Scalars: {number_scalars}"
    )

    # Get scalar information for a certain scalar index.
    (
        return_var,
        name,
        value,
        unit,
    ) = gen.ghs_get_scalar_info(1)
    if return_var != "OK":
        print(f"Failed on GHSGetScalarInfo. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetScalarInfo - Return Status: {return_var}\
        Name: {name}\
        Value: {value}\
        Unit: {unit}"
    )

    # Determine scalar value from a formula name.
    return_var, number_scalars = gen.ghs_get_scalar_value("scalar")
    if return_var != "OK":
        print(f"Failed on GHSGetScalarValue. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetScalarValue - Return Status: {return_var}\
        Formula Name: {number_scalars}"
    )

    # Set a scalar value by formula name.
    return_var = gen.ghs_set_scalar_value("scalar", 10.0)
    if return_var != "OK":
        print(f"Failed on GHSSetScalarValue. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetScalarValue - Return Status: {return_var}")

    # Disconnect
    return_var = gen.ghs_disconnect()
    if return_var != "OK":
        print(f"Failed on GHSDisconnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDisconnect - Return Status: {return_var}")


if __name__ == "__main__":
    main()
