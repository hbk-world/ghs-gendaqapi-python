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

"""Mainframe module interface."""

from .connection import ConnectionHandler
from .ghsapi_states import (
    RETURN_KEY,
    GHSReturnValue,
    GHSSyncStatus,
    GHSUserMode,
    GHSEnableDisable,
    from_string,
    to_string,
)


def get_mainframe_info(
    con_handle: ConnectionHandler,
) -> tuple[str, str | None, str | None, str | None, str | None]:
    """Interface to determine type, name, serial number and firmware
    version information for the connected mainframe.

    The mainframeType, mainframeName, serialNumber and firmwareVersion
    parameters are UTF-8 encoded.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with type, name, serial number and firmware version.
    """

    response_json = con_handle.send_request_wait_response(
        "GetMainframeInformation", None
    )

    if (
        not any(
            key in response_json
            for key in [
                "MainframeType",
                "MainframeName",
                "SerialNumber",
                "FirmwareVersion",
            ]
        )
    ) or (response_json[RETURN_KEY] != GHSReturnValue["OK"]):
        return (
            to_string(response_json[RETURN_KEY], GHSReturnValue),
            None,
            None,
            None,
            None,
        )
    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["MainframeType"],
        response_json["MainframeName"],
        response_json["SerialNumber"],
        response_json["FirmwareVersion"],
    )


def get_disk_space(
    con_handle: ConnectionHandler,
) -> tuple[str, float | None, float | None]:
    """Interface to get total and available mainframe internal disk
    space.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status, total and available mainframe internal
       disk.
    """

    response_json = con_handle.send_request_wait_response("DiskSpace", None)

    if (
        not any(
            key in response_json
            for key in [
                "TotalSize",
                "AvailableSize",
            ]
        )
    ) or (response_json[RETURN_KEY] != GHSReturnValue["OK"]):
        return (
            to_string(response_json[RETURN_KEY], GHSReturnValue),
            None,
            None,
        )
    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["TotalSize"],
        response_json["AvailableSize"],
    )


def get_slot_count(
    con_handle: ConnectionHandler,
) -> tuple[str, int | None]:
    """Interface to get the number of slots in the mainframe.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and number of slots in the mainframe.
    """

    response_json = con_handle.send_request_wait_response("GetSlotCount", None)

    if ("SlotCount" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None
    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["SlotCount"],
    )


def get_sync_status(
    con_handle: ConnectionHandler,
) -> tuple[str, str | None]:
    """Interface to determine the mainframe sync status.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and sync status
    """

    response_json = con_handle.send_request_wait_response(
        "GetSyncStatus", None
    )

    if ("SyncStatus" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None
    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["SyncStatus"], GHSSyncStatus),
    )


def get_user_mode(
    con_handle: ConnectionHandler,
) -> tuple[str, str | None]:
    """Interface to retrieve the user mode.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and user mode.
    """

    response_json = con_handle.send_request_wait_response("GetUserMode", None)

    if ("UserMode" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None
    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["UserMode"], GHSUserMode),
    )


def set_user_mode(con_handle: ConnectionHandler, user_mode: str | int) -> str:
    """Interface to set the user mode.

    The system needs to be idle before calling this function.

    Args:
        con_handle: A unique identifier per mainframe connection.
        user_mode: The desired user mode.

    Returns:
       String value representing request status.
    """

    if isinstance(user_mode, str) and user_mode in GHSUserMode:
        user_mode_dict = {"UserMode": from_string(user_mode, GHSUserMode)}

    elif isinstance(user_mode, int) and user_mode in GHSUserMode.values():
        user_mode_dict = {"UserMode": user_mode}

    else:
        return "InvalidUserMode"

    response_json = con_handle.send_request_wait_response(
        "SetUserMode", user_mode_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def identify(con_handle: ConnectionHandler, enabled: str | int) -> str:
    """Interface to enable or disable the identification sound of the
    connected mainframe.

    Args:
        con_handle: A unique identifier per mainframe connection.
        identity_flag: Enable or disable flag.

    Returns:
       String value representing request status.
    """

    if not enabled:
        return "NullPtrArgument"

    if (isinstance(enabled, str) and enabled in GHSEnableDisable):
        enabled = from_string(enabled, GHSEnableDisable)

    elif (isinstance(enabled, int) and enabled in GHSEnableDisable.values()):
        pass

    else:
        return "InvalidDataType"

    identify_dict = {
        "Identify": enabled
    }

    response_json = con_handle.send_request_wait_response(
        "Identify", identify_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)
