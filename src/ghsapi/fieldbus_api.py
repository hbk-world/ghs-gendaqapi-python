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

"""FieldBus module interface."""

from .connection import ConnectionHandler
from .ghsapi_states import RETURN_KEY, GHSReturnValue, to_string


def initiate_fieldbus_data_transfer(
    con_handle: ConnectionHandler, update_rate: int
) -> tuple[str, int | None, int | None]:
    """Opens a new connection for the field bus data, and waits for client to
    connect. Once the client connects, if the acquisition state is active,
    data is sent to the client. Otherwise nothing is sent.

    If no formulas are present then you get error code back:
    GHSReturnValue_FieldBusError_NotConfigured if the field bus is already
    initiated then an error code is returned:
    GHSReturnValue_FieldBusError_FieldBusEnabled. To change the update rate
    the field bus needs to be stoped and inititate again with a new update
    rate.

    Args:
        con_handle: The unique connection identifier returned by GHSConnect
        update_rate: (in Hz) The update rate should be a part of the list
        containing the supported update rates.If the update rate selected by
        the user is not supported, the mainframe will adjust the update rate,
        based on a minimum distance from the supported rates and returns back
        to the client.

    Returns:
       Tuple with status, update rate and data count.
    """

    if not update_rate:
        return "NullPtrArgument", None, None

    initiate_fieldbus_dict = {
        "UpdateRate": update_rate,
    }

    response_json = con_handle.send_request_wait_response(
        "InitiateFieldBusDataTransfer", initiate_fieldbus_dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "FieldBusPort",
                "BufferDepth",
                "UpdateRate",
                "DataCount",
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
        response_json["UpdateRate"],
        response_json["DataCount"],
    )


def stop_fieldbus_data_transfer(con_handle: ConnectionHandler) -> str:
    """Closes the socket dedicated for the field bus data and stops
    transfering data. The ring buffer allocated for the transfer data is
    deleted.

    Field bus data transfer must have been initiated before calling this
    function.

    Args:
        con_handle: The unique connection identifier returned by GHSConnect

    Returns:
       String value representing request status.
    """

    response_json = con_handle.send_request_wait_response(
        "StopFieldBusDataTransfer", None
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_fieldbus_data_count(
    con_handle: ConnectionHandler,
) -> tuple[str, int | None]:
    """Gets the number of data that are configured to be sent through the
    field bus, excluding the timestamp.

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: The unique connection identifier returned by GHSConnect

    Returns:
       Tuple with status and number of data that are selected to be published.
    """

    response_json = con_handle.send_request_wait_response(
        "GetFieldBusDataCount", None
    )

    if ("DataCount" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["DataCount"],
    )


def get_fieldbus_data_name_and_unit(
    con_handle: ConnectionHandler, data_index: int
) -> tuple[str, str | None, str | None]:
    """Gets the name of specific field bus data value, by giving the index of
    the data value. The number of data values can be retrieved by
    GHSGetFieldBusDataCount. In case of no formulas (or reserved values
    acquisition state and latency) published, an error code is returned:
    GHSReturnValue_FieldBusError_NoFormulasDeployed.

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        data_index: Zero-based index of the data value.

    Returns:
       Tuple with status, name and unit of the data value.
    """

    if not data_index and data_index != 0:
        return "NullPtrArgument", None, None

    data_info_dict = {
        "DataIndex": data_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetFieldBusDataNameAndUnit", data_info_dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "DataName",
                "DataUnit",
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
        response_json["DataName"],
        response_json["DataUnit"],
    )


def request_fieldbus_snapshot(
    con_handle: ConnectionHandler,
) -> tuple[str, float | None, int | None, list[float] | None]:
    """Request a single snapshot of the field bus data. In this case the
    timestamp received is not grid aligned. If the system is not acquiring the
    method returns an error code:GHSReturnValue_SystemNotRecording In case of
    no formulas you get the error return code back:
    GHSReturnValue_FieldBusError_NotConfigured if the field bus is already
    enabled then this method is not allowed.An error return code is
    returned:FieldBusError_UnavailableFunctionality.

    This method can be called by multiple connected clients at same
    time.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status, timestamp, data count and data.
    """

    response_json = con_handle.send_request_wait_response(
        "RequestSnapshot", None
    )

    if (
        not any(
            key in response_json
            for key in [
                "TimeStamp",
                "DataCount",
                "Data",
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
        response_json["TimeStamp"],
        response_json["DataCount"],
        response_json["Data"],
    )
