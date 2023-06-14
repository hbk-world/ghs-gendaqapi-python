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

"""Predefined configurations module interface."""

from .connection import ConnectionHandler
from .ghsapi_states import (
    RETURN_KEY,
    GHSReturnValue,
    GHSConfigurationType,
    GHSHWCompatibility,
    from_string,
    to_string,
)


def apply_configuration(
    con_handle: ConnectionHandler,
    config_id: int
) -> str:
    """Applies one of the predefined configurations as actual configuration of the mainframe.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        config_id: The configuration identification number.

    Returns:
       String value representing request status.
    """

    if not config_id:
        return "NullPtrArgument", None

    dict = {
        "ConfigurationId": config_id,
    }

    response_json = con_handle.send_request_wait_response(
        "ApplyConfiguration", dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_configuration_info(
    con_handle: ConnectionHandler,
    config_type: str | int,
    config_id: int
) -> tuple[
    str, str | None, str | None, str | None, str | None, str | None, str | None
]:
    """Returns information of a specified configuration.
     * This information consists of mainframe type supported by the configuration,
     * acquisition boards supported by the configuration and a textual description of the configuration.
     *
     * @attention The mainframeType, boards, description and path parameters are UTF-8 encoded.
     * @attention The memory allocated for the returned strings must be freed after use using @ref GHSFree().

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        config_type: The configuration type @ref GHSConfigurationType.
        config_id: The configuration identification number.

    Returns:
       Tuple with status and:
        The type of the mainframe.
        The acquisition boards.
        The configuration description.
        The HW compatibility with the given configurations @ref GHSHWCompatibility.
        The wiring path of the given configuration.
        The schematic path of the given configuration.
    """

    if not config_type or not config_id:
        return "NullPtrArgument", None, None, None, None, None, None

    if isinstance(config_type, str) and config_type in GHSConfigurationType:
        config_type = from_string(config_type, GHSConfigurationType)

    dict = {
        "Section": config_type,
        "ConfigurationId": config_id,
    }

    response_json = con_handle.send_request_wait_response(
        "GetConfigurationInformation", dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "Mainframe",
                "Boards",
                "Description",
                "HWCompatibility",
                "WiringPath",
                "SchematicPath"
            ]
        )
    ) or (response_json[RETURN_KEY] != GHSReturnValue["OK"]):
        return (
            to_string(response_json[RETURN_KEY], GHSReturnValue),
            None,
            None,
            None,
            None,
            None,
            None,
        )

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["Mainframe"],
        response_json["Boards"],
        response_json["Description"],
        to_string(response_json["HWCompatibility"], GHSHWCompatibility),
        response_json["WiringPath"],
        response_json["SchematicPath"],
    )


def get_current_configuration_id(
    con_handle: ConnectionHandler
) -> tuple[str, int | None]:
    """Returns the identification number of the currently loaded configuration.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        config_id: The configuration identification number.

    Returns:
       String value representing request status.
    """

    response_json = con_handle.send_request_wait_response(
        "GetCurrentConfigurationId", None
    )

    if ("ConfigurationId" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["ConfigurationId"]
    )


def get_number_of_configurations(
    con_handle: ConnectionHandler,
    config_type: str | int,
) -> tuple[str, int | None]:
    """Returns the total number of predefined configurations present on the mainframe.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        config_type: The configuration type @ref GHSConfigurationType.

    Returns:
       Tuple with status and the total number of configurations.
    """

    if not config_type:
        return "NullPtrArgument", None

    dict = {
        "Section": config_type
    }

    response_json = con_handle.send_request_wait_response(
        "GetNumberOfConfigurations", dict
    )

    if ("TotalConfigurations" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["TotalConfigurations"]
    )


def get_persisted_configuration_id(
    con_handle: ConnectionHandler
) -> tuple[str, int | None]:
    """Returns the identification number of the currently persisted configuration.
     * This is the configuration loaded when the mainframe starts.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and the configuration identification number.
    """

    response_json = con_handle.send_request_wait_response(
        "GetPersistedConfigurationId", None
    )

    if ("ConfigurationId" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["ConfigurationId"]
    )


def set_persisted_configuration(
    con_handle: ConnectionHandler,
    config_id: int
) -> str:
    """Sets the persisted configuration.
     * This is the configuration loaded when the mainframe starts.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and the configuration identification number.
    """

    if not config_id:
        return "NullPtrArgument", None

    dict = {
        "ConfigurationId": config_id
    }

    response_json = con_handle.send_request_wait_response(
        "SetPersistedConfiguration", dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)