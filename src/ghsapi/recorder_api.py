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

"""Recorder module interface."""

from .connection import ConnectionHandler
from .ghsapi_states import (
    RETURN_KEY,
    GHSDigitalOutMode,
    GHSDigitalOutput,
    GHSEnableDisable,
    GHSReturnValue,
    from_string,
    to_string,
)


def get_channel_count(
    con_handle: ConnectionHandler, slot_id: str
) -> tuple[str, int | None]:
    """Retrieve the number of channels for a recorder.

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and number of channels for the recorder.
    """

    if not slot_id:
        return "NullPtrArgument", None

    channel_count_dict = {
        "SlotId": slot_id,
    }

    response_json = con_handle.send_request_wait_response(
        "GetChannelCount", channel_count_dict
    )

    if ("ChannelCount" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["ChannelCount"],
    )


def get_digital_output(
    con_handle: ConnectionHandler, slot_id: str, digital_output: str | int
) -> tuple[str, str | None]:
    """Retrieve the Digital Output Mode for a specified Output ID in a
    recorder.

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        digital_output: The output number desired.

    Returns:
       Tuple with status and digital output mode for that output.
    """

    if not slot_id or not digital_output:
        return "NullPtrArgument", None

    if isinstance(digital_output, str) and digital_output in GHSDigitalOutput:
        digital_output_dict = {
            "SlotId": slot_id,
            "Output": from_string(digital_output, GHSDigitalOutput),
        }

    elif (
        isinstance(digital_output, int)
        and digital_output in GHSDigitalOutput.values()
    ):
        digital_output_dict = {"SlotId": slot_id, "Output": digital_output}

    else:
        return "InvalidOutputNumber", None

    response_json = con_handle.send_request_wait_response(
        "GetDigitalOutput", digital_output_dict
    )

    if ("DigitalOutMode" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["DigitalOutMode"], GHSDigitalOutMode),
    )


def get_number_analog_channels(
    con_handle: ConnectionHandler,
    slot_id: str,
) -> tuple[str, int | None]:
    """Get number of analog channels in a recorder.

    Read - This method can be called by multiple connected clients at
    same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and the number of analog channels in the recorder
    """

    if not slot_id:
        return "NullPtrArgument", None

    analog_channels_dict = {
        "SlotId": slot_id,
    }

    response_json = con_handle.send_request_wait_response(
        "GetNumberOfAnalogChannels", analog_channels_dict
    )

    if ("NumberOfAnalogChannels" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["NumberOfAnalogChannels"],
    )


def get_number_timer_counter_channels(
    con_handle: ConnectionHandler,
    slot_id: str,
) -> tuple[str, int | None]:
    """Get number of timer counter channels in a recorder.

    Read - This method can be called by multiple connected clients at
    same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and the number of timer counter channels in the recorder
    """

    if not slot_id:
        return "NullPtrArgument", None

    timer_counter_channels_dict = {
        "SlotId": slot_id,
    }

    response_json = con_handle.send_request_wait_response(
        "GetNumberOfTimerCounterChannels", timer_counter_channels_dict
    )

    if ("NumberOfTimerCounterChannels" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["NumberOfTimerCounterChannels"],
    )


def get_recorder_enabled(
    con_handle: ConnectionHandler, slot_id: str
) -> tuple[str, str | None]:
    """Determine if recorder is enabled or disabled.

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and recorder enabled status.
    """

    if not slot_id:
        return "NullPtrArgument", None

    recorder_enabled_dict = {
        "SlotId": slot_id,
    }

    response_json = con_handle.send_request_wait_response(
        "GetRecorderEnabled", recorder_enabled_dict
    )

    if ("IsRecorderEnabled" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["IsRecorderEnabled"], GHSEnableDisable),
    )


def get_recorder_info(
    con_handle: ConnectionHandler, slot_id: str
) -> tuple[str, str | None, str | None, str | None, str | None]:
    """Determine type, name, serial number and firmware version
    information for a recorder.

    The recorderType, recorderName, serialNumber and firmwareVersion
    parameters are UTF-8 encoded.

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and recorder information.
    """

    if not slot_id:
        return "NullPtrArgument", None, None, None, None

    recorder_info_dict = {
        "SlotId": slot_id,
    }

    response_json = con_handle.send_request_wait_response(
        "GetRecorderInformation", recorder_info_dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "RecorderType",
                "RecorderName",
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
        response_json["RecorderType"],
        response_json["RecorderName"],
        response_json["SerialNumber"],
        response_json["FirmwareVersion"],
    )


def get_recorder_sales_type(
    con_handle: ConnectionHandler,
    slot_id: str
) -> tuple[str, str | None]:
    """Determine sales type for a recorder.

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and the sales type of the recorder.
    """

    if not slot_id:
        return "NullPtrArgument", None

    recorder_sales_type_dict = {
        "SlotId": slot_id,
    }

    response_json = con_handle.send_request_wait_response(
        "GetRecorderSalesType", recorder_sales_type_dict
    )

    if ("RecorderSalesType" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["RecorderSalesType"]
    )


def get_sample_rate(
    con_handle: ConnectionHandler, slot_id: str
) -> tuple[str, float | None]:
    """Determine the sample rate for a recorder.

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and sample rate for a recorder.
    """

    if not slot_id:
        return "NullPtrArgument", None

    sample_rate_dict = {
        "SlotId": slot_id,
    }

    response_json = con_handle.send_request_wait_response(
        "GetSampleRate", sample_rate_dict
    )

    if ("SampleRate" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["SampleRate"],
    )


def set_digital_output(
    con_handle: ConnectionHandler,
    slot_id: str,
    digital_output: str | int,
    digital_output_mode: str | int,
) -> str:
    """Set the Digital Output Mode for a specified Output ID in a
    recorder.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        digital_output: The output number desired.
        digital_output_mode: The digital output mode to set on that
        output.

    Returns:
       String value representing request status.
    """

    if not slot_id or not digital_output or not digital_output_mode:
        return "NullPtrArgument"

    if isinstance(digital_output, str) and digital_output in GHSDigitalOutput:
        digital_output = from_string(digital_output, GHSDigitalOutput)

    elif (
        isinstance(digital_output, int)
        and digital_output in GHSDigitalOutput.values()
    ):
        pass

    else:
        return "InvalidOutputNumber"

    if (
        isinstance(digital_output_mode, str)
        and digital_output_mode in GHSDigitalOutMode
    ):
        digital_output_mode = from_string(
            digital_output_mode, GHSDigitalOutMode
        )

    elif (
        isinstance(digital_output_mode, int)
        and digital_output_mode in GHSDigitalOutMode.values()
    ):
        pass

    else:
        return "IncompatibleDigitalOutputMode"

    digital_output_dict = {
        "SlotId": slot_id,
        "DigitalOutMode": digital_output_mode,
        "Output": digital_output,
    }

    response_json = con_handle.send_request_wait_response(
        "SetDigitalOutput", digital_output_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def set_recorder_enabled(
    con_handle: ConnectionHandler,
    slot_id: str,
    enabled: str | int,
) -> str:
    """Enable or disable a recorder.

    The system needs to be idle before calling this function.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        enabled: Set to GHS_Enable/GHS_Disable to enable/disable the
        recorder.

    Returns:
       String value representing request status.
    """

    if not slot_id or not enabled:
        return "NullPtrArgument"

    if isinstance(enabled, str) and enabled in GHSEnableDisable:
        enabled = from_string(enabled, GHSEnableDisable)

    elif isinstance(enabled, int) and enabled in GHSEnableDisable.values():
        pass

    else:
        return "InvalidDataType"

    recorder_enabled_dict = {
        "SlotId": slot_id,
        "EnabledStatus": enabled,
    }

    response_json = con_handle.send_request_wait_response(
        "SetRecorderEnabled", recorder_enabled_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def set_sample_rate(
    con_handle: ConnectionHandler,
    slot_id: str,
    sample_rate: float,
) -> str:
    """Set the sample rate for a recorder.

    The system needs to be idle before calling this function.
    This function overwrites any previously set sample rate setting for
    the specified recorder.
    If the specified sample rate is not supported by the recorder, the
    sample rate is rounded to the nearest supported sample rate.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder to get number of
        channels for (e.g. 'A' for the first slot).
        sample_rate: In samples per second.

    Returns:
       String value representing request status.
    """

    if not slot_id or not sample_rate:
        return "NullPtrArgument"

    if not isinstance(sample_rate, float):
        return "InvalidDataType"

    sample_rate_dict = {
        "SlotId": slot_id,
        "SampleRate": sample_rate,
    }

    response_json = con_handle.send_request_wait_response(
        "SetSampleRate", sample_rate_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)
