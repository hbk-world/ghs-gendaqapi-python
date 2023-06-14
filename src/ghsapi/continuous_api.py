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

"""Continuous module interface."""

from .connection import ConnectionHandler
from .ghsapi_states import (
    RETURN_KEY,
    GHSReturnValue,
    GHSContinuousRecordingMode,
    from_string,
    to_string,
)


def get_continuous_lead_out_time(
    con_handle: ConnectionHandler,
    slot_id: int,
) -> tuple[str, float | None]:
    """Determine the continuous recording lead out time for a recorder.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and the continuous recording mode lead out time (post trigger time) in seconds.
    """

    if not slot_id:
        return "NullPtrArgument", None

    dict = {
        "SlotId": slot_id
    }

    response_json = con_handle.send_request_wait_response(
        "GetContinuousLeadOutTime", dict
    )

    if ("ContinuousLeadOutTime" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["ContinuousLeadOutTime"]
    )


def get_continuous_recording_mode(
    con_handle: ConnectionHandler,
    slot_id: int,
) -> tuple[str, str | None]:
    """Determine the continuous recording mode for a recorder.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and the continuous recording mode @ref GHSContinuousRecordingMode.
    """

    if not slot_id:
        return "NullPtrArgument", None

    dict = {
        "SlotId": slot_id
    }

    response_json = con_handle.send_request_wait_response(
        "GetContinuousRecordingMode", dict
    )

    if ("ContinuousRecordingMode" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["ContinuousRecordingMode"], GHSContinuousRecordingMode)
    )


def get_continuous_time_span(
    con_handle: ConnectionHandler,
    slot_id: int,
) -> tuple[str, float | None]:
    """Determine the continuous recording time span for a recorder.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and the time span in seconds for circular and specified time continuous recording modes
    """

    if not slot_id:
        return "NullPtrArgument", None

    dict = {
        "SlotId": slot_id
    }

    response_json = con_handle.send_request_wait_response(
        "GetContinuousTimeSpan", dict
    )

    if ("ContinuousTimeSpan" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["ContinuousTimeSpan"]
    )


def set_continuous_lead_out_time(
    con_handle: ConnectionHandler,
    slot_id: int,
    lead_out_time: float
) -> str:
    """Sets the continuous recording lead out time for a recorder.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).
        lead_out_time: The desired continuous recording mode lead out time (post trigger time) in seconds.

    Returns:
       String value representing request status.
    """

    if not slot_id or not lead_out_time:
        return "NullPtrArgument"

    dict = {
        "SlotId": slot_id,
        "ContinuousLeadOutTime": lead_out_time
    }

    response_json = con_handle.send_request_wait_response(
        "SetContinuousLeadOutTime", dict
    )

    return (to_string(response_json[RETURN_KEY], GHSReturnValue))


def set_continuous_recording_mode(
    con_handle: ConnectionHandler,
    slot_id: int,
    continuous_mode: str | int
) -> str:
    """Set the continuous recording mode for a recorder.
    
    * The system needs to be idle before calling this function.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).
        continuous_mode: The desired continuous recording mode.

    Returns:
       String value representing request status.
    """

    if not slot_id or not continuous_mode:
        return "NullPtrArgument"

    if isinstance(continuous_mode, str) and continuous_mode in GHSContinuousRecordingMode:
        continuous_mode = from_string(continuous_mode, GHSContinuousRecordingMode)

    elif (
        isinstance(continuous_mode, int) and continuous_mode in GHSContinuousRecordingMode.values()
    ):
        pass

    else:
        return "InvalidContinuousMode"

    dict = {
        "SlotId": slot_id,
        "ContinuousRecordingMode": continuous_mode
    }

    response_json = con_handle.send_request_wait_response(
        "SetContinuousRecordingMode", dict
    )

    return (to_string(response_json[RETURN_KEY], GHSReturnValue))


def set_continuous_time_span(
    con_handle: ConnectionHandler,
    slot_id: int,
    time_span: float
) -> str:
    """Set the continuous recording time span for a recorder.
    
    * The system needs to be idle before calling this function.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).
        time_span: The desired time span in seconds for circular and specified time continuous recording modes.

    Returns:
       String value representing request status.
    """

    if not slot_id or not time_span:
        return "NullPtrArgument"

    dict = {
        "SlotId": slot_id,
        "ContinuousTimeSpan": time_span
    }

    response_json = con_handle.send_request_wait_response(
        "SetContinuousTimeSpan", dict
    )

    return (to_string(response_json[RETURN_KEY], GHSReturnValue))