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

"""Sweep module interface."""

from .connection import ConnectionHandler
from .ghsapi_states import (
    RETURN_KEY,
    GHSReturnValue,
    GHSSweepRecordingMode,
    GHSSweepTriggerMode,
    GHSEnableDisable,
    GHSTriggerArmState,
    from_string,
    to_string,
)


def cmd_trigger_arm(
    con_handle: ConnectionHandler
) -> str:
    """Arm the trigger, so that the next trigger will be accepted.
     * After the next trigger occurred, triggers are disarmed automatically and need to be
     * armed explicitly again using this function.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       String value representing request status.
    """

    response_json = con_handle.send_request_wait_response(
        "TriggerArm", None
    )

    return (to_string(response_json[RETURN_KEY], GHSReturnValue))


def get_number_of_sweeps(
    con_handle: ConnectionHandler,
    slot_id: str,
) -> tuple[str, int | None]:
    """Determine the number of sweeps for a recorder.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and the number of sweeps for the recorder.
    """

    if not slot_id:
        return "NullPtrArgument", None

    dict = {
        "SlotId": slot_id
    }

    response_json = con_handle.send_request_wait_response(
        "GetNumberOfSweeps", dict
    )

    if ("NumberSweeps" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["NumberSweeps"]
    )


def get_sweep_length(
    con_handle: ConnectionHandler,
    slot_id: str,
) -> tuple[str, int | None]:
    """Determine the sweep length in samples for a recorder.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and the sweep length in number of samples.
    """

    if not slot_id:
        return "NullPtrArgument", None

    dict = {
        "SlotId": slot_id
    }

    response_json = con_handle.send_request_wait_response(
        "GetSweepLength", dict
    )

    if ("SweepLength" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["SweepLength"]
    )


def get_sweep_recording_mode(
    con_handle: ConnectionHandler,
    slot_id: str,
) -> tuple[str, str | None]:
    """Determine the number of sweeps for a recorder.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and the sweep recording mode for the recorder @ref GHSSweepRecordingMode.
    """

    if not slot_id:
        return "NullPtrArgument", None

    dict = {
        "SlotId": slot_id
    }

    response_json = con_handle.send_request_wait_response(
        "GetSweepRecordingMode", dict
    )

    if ("SweepMode" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["SweepMode"], GHSSweepRecordingMode)
    )


def get_sweep_trigger_mode(
    con_handle: ConnectionHandler,
    slot_id: str,
) -> tuple[str, str | None]:
    """Gets the sweep trigger mode for a recorder.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and the sweep trigger mode.
    """

    if not slot_id:
        return "NullPtrArgument", None

    dict = {
        "SlotId": slot_id
    }

    response_json = con_handle.send_request_wait_response(
        "GetSweepTriggerMode", dict
    )

    if ("SweepTriggerMode" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["SweepTriggerMode"], GHSSweepTriggerMode)
    )


def get_timeout_trigger_enabled(
    con_handle: ConnectionHandler
) -> tuple[str, str | None]:
    """Retrieve the timeout trigger enabled status.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and the flag to indicate if the feature is on.
    """

    response_json = con_handle.send_request_wait_response(
        "GetTimeoutTriggerEnabled", None
    )

    if ("Enable" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["Enable"], GHSEnableDisable)
    )


def get_timeout_trigger_time(
    con_handle: ConnectionHandler
) -> tuple[str, float | None]:
    """Retrieve the timeout trigger time.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and the timeout trigger time in seconds.
    """

    response_json = con_handle.send_request_wait_response(
        "GetTimeoutTriggerTime", None
    )

    if ("Time" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["Time"]
    )


def get_trigger_arm_enabled(
    con_handle: ConnectionHandler
) -> tuple[str, str | None]:
    """Retrieve trigger arm enabled status for a recorder.
     * When enabled, triggers must be armed explicitly before they will be accepted.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and the flag to indicate if the feature is on.
    """

    response_json = con_handle.send_request_wait_response(
        "GetTriggerArmEnabled", None
    )

    if ("Enable" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["Enable"], GHSEnableDisable)
    )


def get_trigger_arm_state(
    con_handle: ConnectionHandler
) -> tuple[str, str | None]:
    """Retrieve the current trigger arm state.
     * This function can be used to synchronize CmdTriggerArm function calls with the user application.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and the current state of trigger arm (e.g. triggers armed or disarmed).
    """

    response_json = con_handle.send_request_wait_response(
        "GetTriggerArmState", None
    )

    if ("TriggerArmState" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["TriggerArmState"], GHSTriggerArmState)
    )


def get_trigger_position(
    con_handle: ConnectionHandler,
    slot_id: str
) -> tuple[str, float | None]:
    """Retrieve the timeout trigger time.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).

    Returns:
       Tuple with status and the trigger position in percentage (0% to 100%).
    """

    if not slot_id:
        return "NullPtrArgument", None

    dict = {
        "SlotId": slot_id
    }

    response_json = con_handle.send_request_wait_response(
        "GetTriggerPosition", dict
    )

    if ("TriggerPosition" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["TriggerPosition"]
    )


def set_number_of_sweeps(
    con_handle: ConnectionHandler,
    slot_id: str,
    number_of_sweeps: int
) -> str:
    """Sets the number of sweeps for a recorder.
    
    The system needs to be idle before calling this function.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).
        number_of_sweeps: The desired number of sweeps for the recorder.

    Returns:
       String value representing request status.
    """

    if not slot_id or not number_of_sweeps:
        return "NullPtrArgument"

    dict = {
        "SlotId": slot_id,
        "NumberSweeps": number_of_sweeps
    }

    response_json = con_handle.send_request_wait_response(
        "SetNumberOfSweeps", dict
    )

    return (to_string(response_json[RETURN_KEY], GHSReturnValue))


def set_sweep_length(
    con_handle: ConnectionHandler,
    slot_id: str,
    number_of_samples: int
) -> str:
    """Sets the sweep length in samples for a recorder.
    
    The system needs to be idle before calling this function.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).
        number_of_samples: The desired sweep length in number of samples.

    Returns:
       String value representing request status.
    """

    if not slot_id or not number_of_samples:
        return "NullPtrArgument"

    dict = {
        "SlotId": slot_id,
        "SweepLength": number_of_samples
    }

    response_json = con_handle.send_request_wait_response(
        "SetSweepLength", dict
    )

    return (to_string(response_json[RETURN_KEY], GHSReturnValue))


def set_sweep_recording_mode(
    con_handle: ConnectionHandler,
    slot_id: str,
    recording_mode: str | int
) -> str:
    """Sets the sweep recording mode for a recorder.
    
    The system needs to be idle before calling this function.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).
        recording_mode: The desired sweep recording mode for the recorder

    Returns:
       String value representing request status.
    """

    if not slot_id or not recording_mode:
        return "NullPtrArgument"

    if isinstance(recording_mode, str) and recording_mode in GHSSweepRecordingMode:
        recording_mode = from_string(recording_mode, GHSSweepRecordingMode)

    elif isinstance(recording_mode, int) and recording_mode in GHSSweepRecordingMode.values():
        pass

    else:
        return "InvalidDataType"

    dict = {
        "SlotId": slot_id,
        "SweepMode": recording_mode
    }

    response_json = con_handle.send_request_wait_response(
        "SetSweepRecordingMode", dict
    )

    return (to_string(response_json[RETURN_KEY], GHSReturnValue))


def set_sweep_trigger_mode(
    con_handle: ConnectionHandler,
    slot_id: str,
    trigger_mode: str | int
) -> str:
    """Sets the sweep trigger mode for a recorder.
    
    * The system needs to be idle before calling this function.
    * Setting the sweep trigger mode to "stop trigger" disables timeout triggers automatically.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).
        trigger_mode: The sweep trigger mode to be set.

    Returns:
       String value representing request status.
    """

    if not slot_id or not trigger_mode:
        return "NullPtrArgument"

    if isinstance(trigger_mode, str) and trigger_mode in GHSSweepTriggerMode:
        trigger_mode = from_string(trigger_mode, GHSSweepTriggerMode)

    elif isinstance(trigger_mode, int) and trigger_mode in GHSSweepTriggerMode.values():
        pass

    else:
        return "InvalidDataType"

    dict = {
        "SlotId": slot_id,
        "SweepTriggerMode": trigger_mode
    }

    response_json = con_handle.send_request_wait_response(
        "SetSweepTriggerMode", dict
    )

    return (to_string(response_json[RETURN_KEY], GHSReturnValue))


def set_timeout_trigger_enabled(
    con_handle: ConnectionHandler,
    enabled: str | int
) -> str:
    """Enables or disables timeout triggers.
     
    * The system needs to be idle before calling this function.
    * If the sweep trigger mode is set to "stop trigger" then timeout triggers are automatically disabled.
    * This function returns @ref GHSReturnValue_Adapted in case enabling timeout triggers is attempted while
    the current sweep trigger mode is "stop trigger".

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        enabled: Flag to indicate if feature is on.

    Returns:
       String value representing request status.
    """

    if not enabled:
        return "NullPtrArgument"

    if isinstance(enabled, str) and enabled in GHSEnableDisable:
        enabled = from_string(enabled, GHSEnableDisable)

    elif isinstance(enabled, int) and enabled in GHSEnableDisable.values():
        pass

    else:
        return "InvalidDataType"

    dict = {
        "Enable": enabled
    }

    response_json = con_handle.send_request_wait_response(
        "SetTimeoutTriggerEnabled", dict
    )

    return (to_string(response_json[RETURN_KEY], GHSReturnValue))


def set_timeout_trigger_time(
    con_handle: ConnectionHandler,
    time: float
) -> str:
    """Sets the timeout trigger time.
    
    * The system needs to be idle before calling this function.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        time: The timeout trigger time in seconds.

    Returns:
       String value representing request status.
    """

    if not time:
        return "NullPtrArgument"

    dict = {
        "Time": time
    }

    response_json = con_handle.send_request_wait_response(
        "SetTimeoutTriggerTime", dict
    )

    return (to_string(response_json[RETURN_KEY], GHSReturnValue))


def set_trigger_arm_enabled(
    con_handle: ConnectionHandler,
    enabled: str | int
) -> str:
    """Enable or disable trigger arm.
     * When enabled, triggers must be armed explicitly before they will be accepted.
    
    * The system needs to be idle before calling this function.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        enabled: Flag to indicate if feature is on.

    Returns:
       String value representing request status.
    """

    if not enabled:
        return "NullPtrArgument"

    if isinstance(enabled, str) and enabled in GHSEnableDisable:
        enabled = from_string(enabled, GHSEnableDisable)

    elif isinstance(enabled, int) and enabled in GHSEnableDisable.values():
        pass

    else:
        return "InvalidDataType"

    dict = {
        "Enable": enabled
    }

    response_json = con_handle.send_request_wait_response(
        "SetTriggerArmEnabled", dict
    )

    return (to_string(response_json[RETURN_KEY], GHSReturnValue))


def set_trigger_position(
    con_handle: ConnectionHandler,
    slot_id: str,
    trigger_position: float
) -> str:
    """Sets the trigger position percentage for a recorder.
    
    * The system needs to be idle before calling this function.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        slot_id: The slot containing the recorder from which to retrieve
        the number of sweeps (e.g. 'A' for the first slot).
        trigger_position: The desired trigger position in percentage (0% to 100%).

    Returns:
       String value representing request status.
    """

    if not slot_id or not trigger_position:
        return "NullPtrArgument"

    dict = {
        "SlotId": slot_id,
        "TriggerPosition": trigger_position
    }

    response_json = con_handle.send_request_wait_response(
        "SetTriggerPosition", dict
    )

    return (to_string(response_json[RETURN_KEY], GHSReturnValue))