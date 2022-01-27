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

"""Manage recordings module interface."""

from .connection import ConnectionHandler
from .ghsapi_states import (
    RETURN_KEY,
    GHSEnableDisable,
    GHSRecordingDataSource,
    GHSReturnValue,
    GHSStorageLocation,
    from_string,
    to_string,
)


def delete_all_recordings(con_handle: ConnectionHandler) -> str:
    """Interface to deletes all recordings from local mainframe storage

    Recordings are deleted asynchronously.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       String value representing request status.
    """

    response_json = con_handle.send_request_wait_response(
        "DeleteAllRecordings", None
    )
    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def delete_last_recording(con_handle: ConnectionHandler) -> str:
    """Interface to delete the most recent recording from local
    mainframe storage.

    Recordings are deleted asynchronously.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       String value representing request status.
    """

    response_json = con_handle.send_request_wait_response(
        "DeleteLastRecording", None
    )
    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_recording_name(
    con_handle: ConnectionHandler,
) -> tuple[str, str | None, int | None]:
    """Interface to get recording base name and recording index of the
    last recording file.

    The recording base name parameter is UTF-8 encoded.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        Tuple with status, base name and index of the recording file.
    """

    response_json = con_handle.send_request_wait_response(
        "GetRecordingName", None
    )

    if (
        not any(
            key in response_json
            for key in [
                "RecordingIndex",
                "RecordingName",
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
        response_json["RecordingName"],
        response_json["RecordingIndex"],
    )


def set_recording_name(
    con_handle: ConnectionHandler, recording_name: str, recording_index: int
) -> str:
    """Interface to set the recording base name and recording index for
    the next recording file.

    The system needs to be idle before calling this function.
    The recording base name parameter must be UTF-8 encoded.

    Args:
        con_handle: A unique identifier per mainframe connection.
        recording_name: The desired base name of the recording file.
        recording_index: The desired index of the recording file.

    Returns:
       String value representing request status.
    """

    if not recording_name or not recording_index:
        return "NullPtrArgument"

    recording_name_dict = {
        "RecordingBaseName": recording_name,
        "RecordingIndex": recording_index,
    }

    response_json = con_handle.send_request_wait_response(
        "SetRecordingName", recording_name_dict
    )
    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_storage_location(
    con_handle: ConnectionHandler,
) -> tuple[str, str | None]:
    """Interface to retrieve the storage location.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and storage location.
    """

    response_json = con_handle.send_request_wait_response(
        "GetStorageLocation", None
    )

    if ("StorageLocation" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None
    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["StorageLocation"], GHSStorageLocation),
    )


def set_storage_location(
    con_handle: ConnectionHandler, storage_location: str | int
) -> str:
    """Interface to set the storage location.

    The system needs to be idle before calling this function.

    Args:
        con_handle: A unique identifier per mainframe connection.
        storage_location: The desired storage location.

    Returns:
       String value representing request status.
    """

    if not storage_location:
        return "NullPtrArgument"

    if (
        isinstance(storage_location, str)
        and storage_location in GHSStorageLocation
    ):
        storage_loc_dict = {
            "StorageLocation": from_string(
                storage_location, GHSStorageLocation
            )
        }

    elif (
        isinstance(storage_location, int)
        and storage_location in GHSStorageLocation.values()
    ):
        storage_loc_dict = {"StorageLocation": storage_location}

    else:
        return "IncompatibleStorage"

    response_json = con_handle.send_request_wait_response(
        "SetStorageLocation", storage_loc_dict
    )
    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_high_low_rate_storage_enabled(
    con_handle: ConnectionHandler,
    source: str | int,
    slot_id: str,
) -> tuple[str, str | None, str | None]:
    """Interface to retrieve storage enabled status of high and low
    rate data for the specified recording data source.

    Args:
        con_handle: A unique identifier per mainframe connection.
        source: The recording data source to retrieve the storage
        enabled status for.
        slot_id: The slot containing the recorder to retrieve the
        storage enabled status for (e.g. 'A' for the first slot). This
        argument is only evaluated for recorder based data sources.

    Returns:
        Tuple with status, flag to indicate if high and low rate data
        is stored.
    """

    if not source or not slot_id:
        return "NullPtrArgument"

    if isinstance(source, str) and source in GHSRecordingDataSource:
        source_slot_dict = {
            "Source": from_string(source, GHSRecordingDataSource),
            "SlotId": slot_id,
        }

    elif isinstance(source, int) and source in GHSRecordingDataSource.values():
        source_slot_dict = {"Source": source, "SlotId": slot_id}

    else:
        return "InvalidDataType"

    response_json = con_handle.send_request_wait_response(
        "GetHighLowRateStorageEnabled", source_slot_dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "HighRateEnable",
                "LowRateEnable",
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
        to_string(response_json["HighRateEnable"], GHSEnableDisable),
        to_string(response_json["LowRateEnable"], GHSEnableDisable),
    )


def set_high_low_rate_storage_enabled(
    con_handle: ConnectionHandler,
    source: str | int,
    slot_id: str,
    high_rate_enabled: str | int,
    low_rate_enabled: str | int,
) -> str:
    """Interface to enable/disable storage of high and low rate data
    for the specified recording data source.

    The system needs to be idle before calling this function.

    Args:
        con_handle: A unique identifier per mainframe connection.
        source: The recording data source to retrieve the storage
        enabled status for.
        slot_id: The slot containing the recorder to retrieve the
        storage enabled status for (e.g. 'A' for the first slot). This
        argument is only evaluated for recorder based data sources.
        high_rate_enabled: Enable/disable storage of high rate data.
        low_rate_enabled: Enable/disable storage of low rate data.

    Returns:
        String value representing request status.
    """

    if (
        not source
        or not slot_id
        or not high_rate_enabled
        or not low_rate_enabled
    ):
        return "NullPtrArgument"

    if isinstance(source, str) and source in GHSRecordingDataSource:
        source = from_string(source, GHSRecordingDataSource)

    elif isinstance(source, int) and source in GHSRecordingDataSource.values():
        pass

    else:
        return "InvalidDataType"

    if (
        isinstance(high_rate_enabled, str)
        and high_rate_enabled in GHSEnableDisable
    ):
        high_rate_enabled = from_string(high_rate_enabled, GHSEnableDisable)

    elif (
        isinstance(high_rate_enabled, int)
        and high_rate_enabled in GHSEnableDisable.values()
    ):
        pass

    else:
        return "InvalidDataType"

    if (
        isinstance(low_rate_enabled, str)
        and low_rate_enabled in GHSEnableDisable
    ):
        low_rate_enabled = from_string(low_rate_enabled, GHSEnableDisable)

    elif (
        isinstance(low_rate_enabled, int)
        and low_rate_enabled in GHSEnableDisable.values()
    ):
        pass

    else:
        return "InvalidDataType"

    source_slot_dict = {
        "Source": source,
        "SlotId": slot_id,
        "HighRateEnable": high_rate_enabled,
        "LowRateEnable": low_rate_enabled,
    }

    response_json = con_handle.send_request_wait_response(
        "SetHighLowRateStorageEnabled", source_slot_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)
