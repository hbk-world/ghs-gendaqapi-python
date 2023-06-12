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
    GHSAmplifierMode,
    GHSChannelType,
    GHSDirection,
    GHSEnableDisable,
    GHSExcitationType,
    GHSFilterType,
    GHSInputCoupling,
    GHSReturnValue,
    GHSSignalCoupling,
    GHSTimerCounterMode,
    GHSTriggerMode,
    GHSChannelType,
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
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    channel_type: str | int,
) -> tuple[str, str | None]:
    """Determine the name of a channel.

     The channel name is UTF-8 encoded.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The one-based index of the specified channel type to determine
        the name for.
        channel_type: The specific channel type.

    Returns:
       Tuple with status and name of the channel.
    """

    if not slot_id or not channel_index or not channel_type:
        return "NullPtrArgument", None

    if isinstance(channel_type, str) and channel_type in GHSChannelType:
        channel_type = from_string(channel_type, GHSChannelType)

    elif isinstance(channel_type, int) and channel_type in GHSChannelType.values():
        pass

    channel_name_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "ChannelType": channel_type
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
    channel_type: str | int,
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
        channel_index: The one-based index of the specified channel type to set
        the name for.
        channel_type: The specific channel type.
        channel_name: The desired channel name.

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not channel_type or not channel_name:
        return "NullPtrArgument"

    if isinstance(channel_type, str) and channel_type in GHSChannelType:
        channel_type = from_string(channel_type, GHSChannelType)

    elif isinstance(channel_type, int) and channel_type in GHSChannelType.values():
        pass

    channel_name_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "ChannelType": channel_type,
        "ChannelName": channel_name,
    }

    response_json = con_handle.send_request_wait_response(
        "SetChannelName", channel_name_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_channel_storage_enabled(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    channel_type: str | int,
) -> tuple[str, str | None]:
    """Determine if storage is enabled or disabled for a channel.

    Read - This method can be called by multiple connected clients at
    same time

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The one-based index of the specified channel type to determine 
        the storage status for.
        channel_type: The specific channel type.

    Returns:
       Tuple with status and storage enabled status for the channel.
    """

    if not slot_id or not channel_index or not channel_type:
        return "NullPtrArgument", None

    if isinstance(channel_type, str) and channel_type in GHSChannelType:
        channel_type = from_string(channel_type, GHSChannelType)

    elif isinstance(channel_type, int) and channel_type in GHSChannelType.values():
        pass

    channel_enabled_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "ChannelType": channel_type,
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
    channel_type: str | int,
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
        channel_index: The one-based index of the specified channel type to set
        the storage status for.
        channel_type: The specific channel type.
        enabled: The desired storage enabled status for the channel

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not channel_type or not enabled:
        return "NullPtrArgument"

    if isinstance(channel_type, str) and channel_type in GHSChannelType:
        channel_type = from_string(channel_type, GHSChannelType)

    elif isinstance(channel_type, int) and channel_type in GHSChannelType.values():
        pass

    if isinstance(enabled, str) and enabled in GHSEnableDisable:
        enabled = from_string(enabled, GHSEnableDisable)

    elif isinstance(enabled, int) and enabled in GHSEnableDisable.values():
        pass

    else:
        return "InvalidDataType"

    channel_enabled_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "ChannelType": channel_type,
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
    channel_type: str | int,
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
        channel_index: The one-based index of the specified channel type to perform
        the zeroing for.
        channel_type: The specific channel type.
        ezeroing: Zero / Unzero the specific channel.

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not channel_type or not ezeroing:
        return "NullPtrArgument"

    if isinstance(channel_type, str) and channel_type in GHSChannelType:
        channel_type = from_string(channel_type, GHSChannelType)

    elif isinstance(channel_type, int) and channel_type in GHSChannelType.values():
        pass

    if isinstance(ezeroing, str) and ezeroing in GHSEnableDisable:
        ezeroing = from_string(ezeroing, GHSEnableDisable)

    elif isinstance(ezeroing, int) and ezeroing in GHSEnableDisable.values():
        pass

    else:
        return "InvalidDataType"

    ezeroing_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "ChannelType": channel_type,
        "ZeroingMode": ezeroing,
    }

    response_json = con_handle.send_request_wait_response(
        "Zeroing", ezeroing_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


## Modules

# Analog


def get_trigger_settings(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[
    str, str | None, float | None, float | None, float | None, str | None
]:
    """Determine the trigger settings for an analog channel.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status and trigger settings.
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None, None, None, None, None

    trigger_settings_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetTriggerSettings", trigger_settings_dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "TriggerMode",
                "PrimaryLevel",
                "SecondaryLevel",
                "Hysteresis",
                "Direction",
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
        )

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["TriggerMode"], GHSTriggerMode),
        response_json["PrimaryLevel"],
        response_json["SecondaryLevel"],
        response_json["Hysteresis"],
        to_string(response_json["Direction"], GHSDirection),
    )


def set_trigger_settings(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    trigger_mode: str | int,
    primary_level: float,
    secondary_level: float,
    hysteresis: float,
    direction: str | int,
) -> str:
    """Set the trigger settings for an analog channel.

     The system needs to be idle before calling this function.

     This function overwrites any previously set trigger settings for
     the specified recorder.

     If the specified trigger mode or value is not supported by the
     recorder, the trigger mode remains unchanged or the value is
     rounded to the nearest supported value.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        trigger_mode: Trigger Mode. Default is TriggerMode_Basic
        primary_level: The desired primary trigger level.
        secondary_level: The desired secondary trigger level.
        hysteresis: The desired trigger hysteresis.
        direction: The desired trigger direction.

    Returns:
       String value representing request status.
    """

    if (
        not slot_id
        or not channel_index
        or not trigger_mode
        or not primary_level
        or not secondary_level
        or not hysteresis
        or not direction
    ):
        return "NullPtrArgument"

    if isinstance(trigger_mode, str) and trigger_mode in GHSTriggerMode:
        trigger_mode = from_string(trigger_mode, GHSTriggerMode)

    elif (
        isinstance(trigger_mode, int)
        and trigger_mode in GHSTriggerMode.values()
    ):
        pass

    else:
        return "InvalidDataType"

    if isinstance(direction, str) and direction in GHSDirection:
        direction = from_string(direction, GHSDirection)

    elif isinstance(direction, int) and direction in GHSDirection.values():
        pass

    else:
        return "InvalidDataType"

    trigger_settings_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "TriggerMode": trigger_mode,
        "PrimaryLevel": primary_level,
        "SecondaryLevel": secondary_level,
        "Hysteresis": hysteresis,
        "Direction": direction,
    }

    response_json = con_handle.send_request_wait_response(
        "SetTriggerSettings", trigger_settings_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_signal_coupling(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, str | None]:
    """Determine the signal coupling for an analog channel.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status and signal coupling for an analog channel.
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None

    signal_coupling_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetSignalCoupling", signal_coupling_dict
    )

    if ("SignalCoupling" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["SignalCoupling"], GHSSignalCoupling),
    )


def set_signal_coupling(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    signal_coupling: str | int,
) -> str:
    """Set the signal coupling for an analog channel.

     If the specified signal coupling mode is not supported by the
     recorder, the signal coupling mode remains unchanged.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        signal_coupling: The desired signal coupling.

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not signal_coupling:
        return "NullPtrArgument"

    if (
        isinstance(signal_coupling, str)
        and signal_coupling in GHSSignalCoupling
    ):
        signal_coupling = from_string(signal_coupling, GHSSignalCoupling)

    elif (
        isinstance(signal_coupling, int)
        and signal_coupling in GHSSignalCoupling.values()
    ):
        pass

    else:
        return "InvalidDataType"

    signal_coupling_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "SignalCoupling": signal_coupling,
    }

    response_json = con_handle.send_request_wait_response(
        "SetSignalCoupling", signal_coupling_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_input_coupling(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, str | None]:
    """Determine the input coupling for an analog channel.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status and input coupling for an analog channel.
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None

    input_coupling_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetInputCoupling", input_coupling_dict
    )

    if ("InputCoupling" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["InputCoupling"], GHSInputCoupling),
    )


def set_input_coupling(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    input_coupling: str | int,
) -> str:
    """Set the input coupling for an analog channel.

     The system needs to be idle before calling this function.

     If the specified input coupling mode is not supported by the
     recorder, the input coupling mode remains unchanged.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        input_coupling: The desired input coupling.

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not input_coupling:
        return "NullPtrArgument"

    if isinstance(input_coupling, str) and input_coupling in GHSInputCoupling:
        input_coupling = from_string(input_coupling, GHSInputCoupling)

    elif (
        isinstance(input_coupling, int)
        and input_coupling in GHSInputCoupling.values()
    ):
        pass

    else:
        return "InvalidDataType"

    input_coupling_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "InputCoupling": input_coupling,
    }

    response_json = con_handle.send_request_wait_response(
        "SetInputCoupling", input_coupling_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_span_and_offset(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, float | None, float | None]:
    """Determine the span and offset for an analog channel.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status, span and offset for an analog channel.
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None, None

    span_offset_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetSpanAndOffset", span_offset_dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "Span",
                "Offset",
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
        response_json["Span"],
        response_json["Offset"],
    )


def set_span_and_offset(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    span: float,
    offset: float,
) -> str:
    """Set Span and offset for analog channels.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        span: The span in user units. The value is adapted to available
        options.
        offset: The offset in user units. The value is adapted to
        available options.

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not span or not offset:
        return "NullPtrArgument"

    if not (isinstance(span, float) and isinstance(offset, float)):
        return "InvalidDataType"

    span_offset_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "Span": span,
        "Offset": offset,
    }

    response_json = con_handle.send_request_wait_response(
        "SetSpanAndOffset", span_offset_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_filter_type_and_frequency(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, str | None, float | None]:
    """Determine the filter type and frequency for an analog channel.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status, filter type and frequency for an analog
       channel.
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None, None

    filter_freq_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetFilterTypeAndFrequency", filter_freq_dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "FilterType",
                "Frequency",
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
        to_string(response_json["FilterType"], GHSFilterType),
        response_json["Frequency"],
    )


def set_filter_type_and_frequency(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    filter_type: str | int,
    frequency: float,
) -> str:
    """Set the filter type and frequency for an analog channel.

     This function overwrites any previously set filter settings for
     the specified recorder.

     If the specified filter type or value is not supported by the
     recorder, the filter type remains unchanged or the value is
     rounded to the nearest supported value.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        filter_type: The filter type. Default is GHSFilterType_Bessel.
        frequency: The filter frequency in Hz.

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not filter_type or not frequency:
        return "NullPtrArgument"

    if isinstance(filter_type, str) and filter_type in GHSFilterType:
        filter_type = from_string(filter_type, GHSFilterType)

    elif (
        isinstance(filter_type, int) and filter_type in GHSFilterType.values()
    ):
        pass

    else:
        return "InvalidDataType"

    if not isinstance(frequency, float):
        return "InvalidDataType"

    filter_freq_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "FilterType": filter_type,
        "Frequency": frequency,
    }

    response_json = con_handle.send_request_wait_response(
        "SetFilterTypeAndFrequency", filter_freq_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_excitation(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, str | None, float | None]:
    """Determine the excitation type and value for an analog channel.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status, excitation type and excitation value
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None, None

    excitation_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetExcitation", excitation_dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "ExcitationType",
                "ExcitationValue",
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
        to_string(response_json["ExcitationType"], GHSExcitationType),
        response_json["ExcitationValue"],
    )


def set_excitation(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    excitation_type: str | int,
    excitation_value: float,
) -> str:
    """Set the excitation type and value for an analog channel.

     The system needs to be idle before calling this function.

     If the specified excitation type or value is not supported by the
     recorder, the excitation type remains unchanged or the value is rounded
     to the nearest supported value.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        excitation_type: The desired excitation type. Default is
        ExcitationType_Voltage.
        excitation_value: The desired excitation value in user units (voltage
        or current).

    Returns:
       String value representing request status.
    """

    if (
        not slot_id
        or not channel_index
        or not excitation_type
        or not excitation_value
    ):
        return "NullPtrArgument"

    if (
        isinstance(excitation_type, str)
        and excitation_type in GHSExcitationType
    ):
        excitation_type = from_string(excitation_type, GHSExcitationType)

    elif (
        isinstance(excitation_type, int)
        and excitation_type in GHSExcitationType.values()
    ):
        pass

    else:
        return "InvalidDataType"

    if not isinstance(excitation_value, float):
        return "InvalidDataType"

    excitation_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "ExcitationType": excitation_type,
        "ExcitationValue": excitation_value,
    }

    response_json = con_handle.send_request_wait_response(
        "SetExcitation", excitation_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_amplifier_mode(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, str | None]:
    """Determine the amplifier mode for an analog channel.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status and amplifier mode
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None

    amplifier_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetAmplifierMode", amplifier_dict
    )

    if ("AmplifierMode" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return (
            to_string(response_json[RETURN_KEY], GHSReturnValue),
            None,
        )

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["AmplifierMode"], GHSAmplifierMode),
    )


def set_amplifier_mode(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    amplifier_mode: str | int,
) -> str:
    """Set the amplifier mode for an analog channel.

     The system needs to be idle before calling this function.

     If the specified amplifier mode is not supported by the recorder, the
     amplifier mode remains unchanged.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        amplifier_mode: The desired amplifier mode

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not amplifier_mode:
        return "NullPtrArgument"

    if isinstance(amplifier_mode, str) and amplifier_mode in GHSAmplifierMode:
        amplifier_mode = from_string(amplifier_mode, GHSAmplifierMode)

    elif (
        isinstance(amplifier_mode, int)
        and amplifier_mode in GHSAmplifierMode.values()
    ):
        pass

    else:
        return "InvalidDataType"

    amplifier_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "AmplifierMode": amplifier_mode,
    }

    response_json = con_handle.send_request_wait_response(
        "SetAmplifierMode", amplifier_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_technical_units(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, str | None, float | None, float | None]:
    """Determine the technical units, unit multiplier and unit offset for an
    analog channel.

    The units parameter is UTF-8 encoded.

    Read - This method can be called by multiple connected clients at
    same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status, technical units, technical units multiplier value
       and technical units offset value.
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None, None, None

    technical_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetTechnicalUnits", technical_dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "Multiplier",
                "Offset",
                "UnitType",
            ]
        )
    ) or (response_json[RETURN_KEY] != GHSReturnValue["OK"]):
        return (
            to_string(response_json[RETURN_KEY], GHSReturnValue),
            None,
            None,
            None,
        )

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["UnitType"],
        response_json["Multiplier"],
        response_json["Offset"],
    )


def set_technical_units(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    units: str,
    multiplier: float,
    offset: float,
) -> str:
    """Set the technical units, unit multiplier and unit offset for an analog
    channel.

     The units parameter is UTF-8 encoded.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        units: The desired technical units (e.g. 'V' for Volt or 'Hz' for
        Hertz).
        multiplier: The desired technical units multiplier value.
        offset: The desired technical units offset value.

    Returns:
       String value representing request status.
    """

    if (
        not slot_id
        or not channel_index
        or not units
        or not multiplier
        or not offset
    ):
        return "NullPtrArgument"

    if (
        not isinstance(units, str)
        or not isinstance(multiplier, float)
        or not isinstance(offset, float)
    ):
        return "InvalidDataType"

    technical_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "UnitType": units,
        "Multiplier": multiplier,
        "Offset": offset,
    }

    response_json = con_handle.send_request_wait_response(
        "SetTechnicalUnits", technical_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_auto_range(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, str | None, float | None]:
    """Determine the auto range enable and time settings.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status, auto range enabled setting and time for auto range
       in seconds
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None, None

    auto_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetAutoRange", auto_dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "AutoRangeEnabled",
                "AutoRangeTime",
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
        to_string(response_json["AutoRangeEnabled"], GHSEnableDisable),
        response_json["AutoRangeTime"],
    )


def set_auto_range(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    auto_range_enabled: str | int,
    auto_range_time: float,
) -> str:
    """Set Auto range settings for analog channels.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        auto_range_enabled: The auto range enabled setting. The value is
        adapted to available options.
        auto_range_time: The time for auto range in seconds. The value is
        adapted to available options.

    Returns:
       String value representing request status.
    """

    if (
        not slot_id
        or not channel_index
        or not auto_range_enabled
        or not auto_range_time
    ):
        return "NullPtrArgument"

    if (
        isinstance(auto_range_enabled, str)
        and auto_range_enabled in GHSEnableDisable
    ):
        auto_range_enabled = from_string(auto_range_enabled, GHSEnableDisable)

    elif (
        isinstance(auto_range_enabled, int)
        and auto_range_enabled in GHSEnableDisable.values()
    ):
        pass

    else:
        return "InvalidDataType"

    if not isinstance(auto_range_time, float):
        return "InvalidDataType"

    auto_range_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "AutoRangeEnabled": auto_range_enabled,
        "AutoRangeTime": auto_range_time,
    }

    response_json = con_handle.send_request_wait_response(
        "SetAutoRange", auto_range_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def cmd_auto_range_now(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    auto_range_time: float,
) -> str:
    """Command a single shot for auto range.

     The system needs to be acquiring for this function to have any effect.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        auto_range_time: The time for auto range in seconds. The value is
        adapted to available options.

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not auto_range_time:
        return "NullPtrArgument"

    if not isinstance(auto_range_time, float):
        return "InvalidDataType"

    auto_range_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "AutoRangeTime": auto_range_time,
    }

    response_json = con_handle.send_request_wait_response(
        "AutoRangeNow", auto_range_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_channel_cal_info(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[
    str, str | None, str | None, str | None, str | None, str | None, str | None
]:
    """Retrieve calibration information for an analog channel.

    The calibrationDateTime, verificationDateTime, powerVerificationDateTime,
    calibrationLab, verificationLab and powerVerificationLab parameters are
    UTF-8 encoded.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status and calibration information
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None, None, None, None, None, None

    cal_info_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetChannelCalibrationInformation", cal_info_dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "CalibrationDateTime",
                "VerificationDateTime",
                "PowerVerificationDateTime",
                "CalibrationLab",
                "VerificationLab",
                "PowerVerificationLab",
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
        response_json["CalibrationDateTime"],
        response_json["VerificationDateTime"],
        response_json["PowerVerificationDateTime"],
        response_json["CalibrationLab"],
        response_json["VerificationLab"],
        response_json["PowerVerificationLab"],
    )


# Timer/Counter


def get_timer_counter_gate_time(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, float | None]:
    """Determine the gate time for a timer/counter channel.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status and the gate time in seconds.
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None

    gate_time_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetTimerCounterGateTime", gate_time_dict
    )

    if ("GateTime" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return (
            to_string(response_json[RETURN_KEY], GHSReturnValue),
            None,
        )

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["GateTime"],
    )


def set_timer_counter_gate_time(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    gate_time: float,
) -> str:
    """Set the gate time for a timer/counter channel.

     The system needs to be idle before calling this function.

     If the specified timer/counter gate time is not supported by the
     recorder, the timer/counter gate time is rounded to the nearest supported
     gate time.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        gate_time: The desired gate time in seconds.

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not gate_time:
        return "NullPtrArgument"

    if not isinstance(gate_time, float):
        return "InvalidDataType"

    gate_time_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "GateTime": gate_time,
    }

    response_json = con_handle.send_request_wait_response(
        "SetTimerCounterGateTime", gate_time_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_timer_counter_mode(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, str | None]:
    """Determine the mode for a timer/counter channel.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status and the timer/counter mode
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None

    mode_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetTimerCounterMode", mode_dict
    )

    if ("TimerCounterMode" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return (
            to_string(response_json[RETURN_KEY], GHSReturnValue),
            None,
        )

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["TimerCounterMode"], GHSTimerCounterMode),
    )


def set_timer_counter_mode(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    mode: str | int,
) -> str:
    """Set the mode for a timer/counter channel.

     The system needs to be idle before calling this function.

     If the specified timer/counter mode is not supported by the recorder, the
     timer/counter mode remains unchanged.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        mode: The desired timer/counter mode. Default is
        TimerCounterMode_RPMUniDirectional.

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not mode:
        return "NullPtrArgument"

    if isinstance(mode, str) and mode in GHSTimerCounterMode:
        mode = from_string(mode, GHSTimerCounterMode)

    elif isinstance(mode, int) and mode in GHSTimerCounterMode.values():
        pass

    else:
        return "InvalidDataType"

    mode_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "TimerCounterMode": mode,
    }

    response_json = con_handle.send_request_wait_response(
        "SetTimerCounterMode", mode_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_timer_counter_range(
    con_handle: ConnectionHandler, slot_id: str, channel_index: int
) -> tuple[str, float | None, float | None]:
    """Determine the range for a timer/counter channel.

    Read - This method can be called by multiple connected clients at
    same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.

    Returns:
       Tuple with status, the lower range value and the upper range value.
    """

    if not slot_id or not channel_index:
        return "NullPtrArgument", None, None

    range_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetTimerCounterRange", range_dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "UpperValue",
                "LowerValue",
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
        response_json["LowerValue"],
        response_json["UpperValue"],
    )


def set_timer_counter_range(
    con_handle: ConnectionHandler,
    slot_id: str,
    channel_index: int,
    lower_value: float,
    upper_value: float,
) -> str:
    """Set the range for a timer/counter channel.

     The system needs to be idle before calling this function.

     If the specified timer/counter range is illegal (i.e. upperValue <
     lowerValue), the timer/counter range values are corrected to the nearest
     possible values.

     ReadWrite - This method will only process requests from the
     connected client with the most privileges order (Privileges order:
     1- Perception, 2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        channel_index: The zero-based index of the channel to determine
        the type for.
        lower_value: The desired lower range value.
        upper_value: The desired upper range value.

    Returns:
       String value representing request status.
    """

    if not slot_id or not channel_index or not lower_value or not upper_value:
        return "NullPtrArgument"

    if not isinstance(lower_value, float) or not isinstance(
        upper_value, float
    ):
        return "InvalidDataType"

    range_dict = {
        "SlotId": slot_id,
        "ChannelIndex": channel_index,
        "UpperValue": upper_value,
        "LowerValue": lower_value,
    }

    response_json = con_handle.send_request_wait_response(
        "SetTimerCounterRange", range_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)
