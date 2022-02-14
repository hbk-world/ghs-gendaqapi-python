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

"""Channel module interface."""

from .connection import ConnectionHandler
from .ghsapi_states import (
    RETURN_KEY,
    GHSChannelType,
    GHSEnableDisable,
    GHSReturnValue,
    from_string,
    to_string,
)

# Functions


def get_channel_type(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, str | None]:
    """Determine the type of a channel.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status and type of the channel.
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None

    channel_type_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetChannelType", channel_type_dict
    )

    if ("ChannelType" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["ChannelType"], GHSChannelType),
    )


def get_channel_name(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, str | None]:
    """Determine the name of a channel.

     The channel name is UTF-8 encoded.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status and name of the channel.
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None

    channel_name_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetChannelName", channel_name_dict
    )

    if ("ChannelName" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["ChannelName"],
    )


def set_channel_name(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    channel_name: str,
) -> str:
    """Set the name of a channel.

     The channel name is UTF-8 encoded.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        channel_name: The desired channel name.

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not channel_name:
        return "NullPtrArgument"

    channel_name_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "ChannelName": channel_name,
    }

    response_json = con_handle.send_request_wait_response(
        "SetChannelName", channel_name_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_channel_storage_enabled(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, str | None]:
    """Determine if storage is enabled or disabled for a channel.

    Read - This method can be called by multiple connected clients at
    same time

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status and storage enabled status for the channel.
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None

    channel_enabled_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetChannelStorageEnabled", channel_enabled_dict
    )

    if ("Enabled" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["Enabled"], GHSEnableDisable),
    )


def set_channel_storage_enabled(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    enabled: str | int,
) -> str:
    """Enable or disable storage for a channel.

    The system needs to be idle before calling this function.

    ReadWrite - This method will only process requests from the
    connected client with the most privileges order (Privileges order:
    1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        enabled: The desired storage enabled status for the channel

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not enabled:
        return "NullPtrArgument"

    if isinstance(enabled, str) and enabled in GHSEnableDisable:
        enabled = from_string(enabled, GHSEnableDisable)

    elif isinstance(enabled, int) and enabled in GHSEnableDisable.values():
        pass

    else:
        return "InvalidDataType"

    channel_enabled_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "ChannelStorageEnable": enabled,
    }

    response_json = con_handle.send_request_wait_response(
        "SetChannelStorageEnabled", channel_enabled_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def cmd_zeroing(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    ezeroing: str | int,
) -> str:
    """Perform zeroing in a channel.

     The system needs to be idle before calling this function.

     Read - This method can be called by multiple connected clients at
     same time

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        ezeroing: Zero / Unzero the specific channel.

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not ezeroing:
        return "NullPtrArgument"

    if isinstance(ezeroing, str) and ezeroing in GHSEnableDisable:
        ezeroing = from_string(ezeroing, GHSEnableDisable)

    elif isinstance(ezeroing, int) and ezeroing in GHSEnableDisable.values():
        pass

    else:
        return "InvalidDataType"

    ezeroing_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "ZeroingMode": ezeroing,
    }

    response_json = con_handle.send_request_wait_response(
        "Zeroing", ezeroing_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)
