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

    # Applies one of the predefined configurations as actual configuration of the mainframe
    return_var = gen.ghs_apply_configuration(1)
    if return_var != "OK":
        print(f"Failed on GHSApplyConfiguration. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSApplyConfiguration - Return Status: {return_var}"
    )

    # Returns information of a specified configuration
    (
        return_var,
        mainframe,
        boards,
        description,
        hw_compatibility,
        wiring_path,
        schematic_path,
    ) = gen.ghs_get_configuration_info("User", 1)
    if return_var != "OK":
        print(f"Failed on GHSGetConfigurationInformation. Return Status: {return_var}")
        sys.exit()
    print(f"GHSGetConfigurationInformation - Return Status: {return_var}\
        Mainframe: {mainframe}\
        Boards: {boards}\
        Description: {description}\
        HWCompatibility: {hw_compatibility}\
        WiringPath: {wiring_path}\
        SchematicPath: {schematic_path}"
    )

    # Returns the identification number of the currently loaded configuration
    return_var, config_id = gen.ghs_get_current_configuration_id()
    if return_var != "OK":
        print(f"Failed on GHSGetCurrentConfigurationId. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetCurrentConfigurationId - Return Status: {return_var}\
        ConfigurationId: {config_id}"
    )

    # Returns the total number of predefined configurations present on the mainframe
    return_var, number_configs = gen.ghs_get_number_of_configurations("User")
    if return_var != "OK":
        print(f"Failed on GHSGetCurrentConfigurationId. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetNumberOfConfigurations - Return Status: {return_var}\
        TotalConfigurations: {number_configs}"
    )

    # Returns the total number of predefined configurations present on the mainframe
    return_var, config_id = gen.ghs_get_persisted_configuration_id()
    if return_var != "OK":
        print(f"Failed on GHSGetPersistedConfigurationId. Return Status: {return_var}")
        sys.exit()
    print(
        f"GHSGetPersistedConfigurationId - Return Status: {return_var}\
        ConfigurationId: {config_id}"
    )

    # Set sample rate
    return_var = gen.ghs_set_persisted_configuration(1)
    if return_var != "OK":
        print(f"Failed on GHSSetPersistedConfiguration. Return Status: {return_var}")
        sys.exit()
    print(f"GHSSetPersistedConfiguration - Return Status: {return_var}")

    # Disconnect
    return_var = gen.ghs_disconnect()
    if return_var != "OK":
        print(f"Failed on GHSDisconnect. Return Status: {return_var}")
        sys.exit()
    print(f"GHSDisconnect - Return Status: {return_var}")


if __name__ == "__main__":
    main()
