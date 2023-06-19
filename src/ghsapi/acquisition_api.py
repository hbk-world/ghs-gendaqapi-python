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

"""Acquisition control module interface.

It is used to control acquisition state of the mainframe.
"""

from .connection import ConnectionHandler
from .ghsapi_states import (
    RETURN_KEY,
    GHSAcquisitionState,
    GHSExtendedAcquisitionState,
    GHSReturnValue,
    to_string,
)


def start_preview(con_handle: ConnectionHandler) -> str:
    """Interface to start preview mode.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        String value representing request status.
    """

    response_json = con_handle.send_request_wait_response("StartPreview", None)
    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def stop_preview(con_handle: ConnectionHandler) -> str:
    """Interface to stop preview mode.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        An String value representing request status.
    """

    response_json = con_handle.send_request_wait_response("StopPreview", None)
    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def start_recording(con_handle: ConnectionHandler) -> str:
    """Interface to start recording on local storage.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        String value representing request status.
    """

    recording_dict = {
        "IgnoreSync": 0
    }

    response_json = con_handle.send_request_wait_response(
        "StartRecording", recording_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def start_recording_without_synch_check(con_handle: ConnectionHandler) -> str:
    """Interface to start recording on local storage without checking synchronization status.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        String value representing request status.
    """

    recording_dict = {
        "IgnoreSync": 1
    }

    response_json = con_handle.send_request_wait_response(
        "StartRecording", recording_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def start_recording_in_pause(
    con_handle: ConnectionHandler,
    ignore_sync: int
) -> str:
    """Starts a recording on local storage in Pause mode.
     *
     * The system needs to be idle before calling this function.
     * Note that the connected mainframe will generate a recording name.
     * This command can be executed only successfully when the local storage is set.
     * Execution of this command can be influenced by Perception setting "Suspend storage at start of recording"

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        ignore_sync: Flag (0/1) to indicate if mainframe synchronization check will be ignored.

    Returns:
        String value representing request status.
    """

    if not ignore_sync:
        return "NullPtrArgument"

    recording_in_pause_dict = {
        "IgnoreSync": ignore_sync,
        "StartPaused": 1,
    }

    response_json = con_handle.send_request_wait_response(
        "StartRecording", recording_in_pause_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def pause_recording(con_handle: ConnectionHandler) -> str:
    """Interface to pause a started recording.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        String value representing request status.
    """

    response_json = con_handle.send_request_wait_response(
        "PauseRecording", None
    )
    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def resume_recording(con_handle: ConnectionHandler) -> str:
    """Interface to resume a paused recording.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        String value representing request status.
    """

    response_json = con_handle.send_request_wait_response(
        "ResumeRecording", None
    )
    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def stop_recording(con_handle: ConnectionHandler) -> str:
    """Interface to stop a started recording.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        String value representing request status.
    """

    response_json = con_handle.send_request_wait_response(
        "StopRecording", None
    )
    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def trigger(con_handle: ConnectionHandler) -> str:
    """Interface to issue a trigger.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        String value representing request status.
    """

    response_json = con_handle.send_request_wait_response("Trigger", None)
    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_acquisition_state(
    con_handle: ConnectionHandler,
) -> tuple[str, str | None]:
    """Interface to get acquisition state of mainframe.

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        Tuple with status and acquisition state of the mainframe.
    """

    response_json = con_handle.send_request_wait_response(
        "GetAcquisitionState", None
    )
    if ("GHSAcquisitionState" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None
    return to_string(response_json[RETURN_KEY], GHSReturnValue), to_string(
        response_json["GHSAcquisitionState"], GHSAcquisitionState
    )


def get_acquisition_start_time(
    con_handle: ConnectionHandler,
) -> tuple[str, int | None, int | None, float | None]:
    """Interface to get absolute time of the start of acquisition.

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        Tuple with status and the absolute time of the start of
        acquisition.
    """

    response_json = con_handle.send_request_wait_response(
        "GetAcquisitionStartTime", None
    )

    if (
        not any(
            key in response_json
            for key in [
                "AbsoluteTimeYear",
                "AbsoluteTimeDay",
                "AbsoluteTimeSeconds",
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
        response_json["AbsoluteTimeYear"],
        response_json["AbsoluteTimeDay"],
        response_json["AbsoluteTimeSeconds"],
    )


def get_acquisition_time(
    con_handle: ConnectionHandler,
) -> tuple[str, float | None]:
    """Interface to get current acquisition time relative to the start
    of acquistion.

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and current acquisition time relative to
       the start of acquistion.
    """

    response_json = con_handle.send_request_wait_response(
        "GetAcquisitionTime", None
    )

    if ("AcquisitionTime" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None
    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["AcquisitionTime"],
    )


def get_extended_acquisition_state(
    con_handle: ConnectionHandler,
) -> tuple[str, str | None, int | None]:
    """Returns the extended Acquisition State of the Mainframe.
    This includes sweep state and trigger count.

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        Tuple with status, acquisition state of the mainframe and trigger count.
    """

    response_json = con_handle.send_request_wait_response(
        "GetAcquisitionState", None
    )
    if ("GHSExtendedAcquisitionState" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None
    
    return(
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["GHSAcquisitionState"], GHSExtendedAcquisitionState),
        response_json["TriggerCount"]
    )