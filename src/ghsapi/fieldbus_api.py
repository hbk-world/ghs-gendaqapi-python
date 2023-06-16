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

import sys
import struct

from .connection import ConnectionHandler
from .fieldbus_ringbuffer import FieldBusData
from .fieldbus_ringbuffer import FieldBus
from .ghsapi_states import (
    RETURN_KEY,
    GHSReturnValue,
    GHSFunctionCallType,
    to_string,
    from_string
)

SIZE_OF_FLOAT = 4
SIZE_OF_DOUBLE = 8

def initiate_fieldbus_data_transfer(
    con_handle: ConnectionHandler, update_rate: int, fieldbus_handle: FieldBus
) -> tuple[str, int | None, int | None]:
    """Opens a new connection for the field bus data, and waits for client to
    connect. Once the client connects, if the acquisition state is active,
    data is sent to the client. Otherwise nothing is sent.

    * If no formulas are present then you get error code back:
    GHSReturnValue_FieldBusError_NotConfigured

    * If the field bus is already initiated then an error code is returned:
    GHSReturnValue_FieldBusError_FieldBusEnabled.

    *To change the update rate the field bus needs
    to be stoped and inititate again with a new update rate.

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

    bufferDepth = response_json["BufferDepth"]
    dataCount = response_json["DataCount"]
    fieldBusPort = response_json["FieldBusPort"]
    fieldbus_handle.__init__(bufferDepth, dataCount)
    if not fieldbus_handle.dataHandle:
        return "FieldBusError_NullFieldBusRingBuffer", None, None

    ConnectionHandler.connection_establish (
        fieldbus_handle.conHandle,
        fieldbus_handle.ipAddress,
        fieldBusPort
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

    * Fieldbus data transfer must have been initiated before calling this
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
    """Gets the number of data that are configured to be sent through the field bus, excluding the timestamp.

    *The number of data values can be retrieved by ghs_get_fieldbus_data_count().

    *Read - This method can be called by multiple connected clients at same
    time.*

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and total number of fieldbus data channel being published.
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
    """Gets the name of specific field bus data value, by giving the index of the data value.

    *The number of data values can be retrieved by ghs_get_fieldbus_data_count().

    *In case of no formulas (or reserved values acquisition state and latency) published,
    an error code is returned: FieldBusError_NoFormulasDeployed.

    *Read - This method can be called by multiple connected clients at same
    time.*

    Args:
        con_handle: A unique identifier per mainframe connection.
        data_index: Zero-based index of the data value.

    Returns:
       Tuple with status, data name and data unit for the desired fieldbus index.
    """

    if data_index < 0:
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
    dataCount: int
) -> tuple[str, float | None, int | None, list[float] | None]:
    """ Request a single snapshot of the field bus data.

    *In this case the timestamp received is not grid aligned.

    *If the system is not acquiring the method returns an error code: SystemNotRecording

    *In case of no formulas you get the error return code back: FieldBusError_NotConfigured

    *If the fieldbus is already enabled then this method is not allowed.
    An error return code is returned: FieldBusError_FieldBusAlready_Enabled

    *Read - This method can be called by multiple connected clients at same
    time.*

    Args:
        con_handle: A unique identifier per mainframe connection.
        data_index: Zero-based index of the data value.

    Returns:
       Tuple with status, timestamp, total number of fieldbus channels and the fieldbus data.
    """

    if not dataCount:
        return "NullPtrArgument", None, None, None

    nClientAllocatedDataSize = dataCount

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

    dataCount = response_json["DataCount"]
    if nClientAllocatedDataSize < dataCount:
        return "FieldBusError_BufferSizeInvalid"

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["TimeStamp"],
        response_json["DataCount"],
        response_json["Data"],
    )


def receive_fieldbus_data(
    fieldbus_handle: FieldBus
) -> str:
    """Used to retrieve the FieldBus data from the new socket connection and write on the buffer.

    *Can be used in a thread and if so, mutual exclusion should be used with GHSStopFieldBusDataTransfer.

    *This function should be used in a loop if continuous delivery of Async Data is desired.

    *Field bus data transfer must have been initiated before calling this function.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       String value representing request status.
    """

    if not fieldbus_handle:
        return GHSReturnValue["NotConnected"]

    packetSize = fieldbus_handle.dataHandle.data_count

    packet = FieldBusData(packetSize)

    fieldBusPacketSize = SIZE_OF_DOUBLE + SIZE_OF_FLOAT * packetSize
    returnTuple = connection_read_raw(fieldbus_handle, fieldBusPacketSize)
    returnValue = returnTuple[0]
    if (returnValue != GHSReturnValue["OK"]):
        return returnValue

    fieldBusStream = returnTuple[1]
    packet.timeStamp = struct.unpack('d', fieldBusStream[:SIZE_OF_DOUBLE])[0]
    byte_index = SIZE_OF_DOUBLE
    if packet.fValues:
        while byte_index < fieldBusPacketSize:
            values_index = int(byte_index / SIZE_OF_FLOAT) - 2
            data_string = fieldBusStream[byte_index:byte_index + SIZE_OF_FLOAT]
            packet.fValues[values_index] = struct.unpack('f', fieldBusStream[byte_index:byte_index + SIZE_OF_FLOAT])[0]
            byte_index += SIZE_OF_FLOAT

    fieldbus_handle.dataHandle.put_data(packet.timeStamp, packet.fValues)

    return to_string(returnValue, GHSReturnValue)


def connection_read_raw(fieldbus: FieldBus, size) -> tuple[int | None, bytes | None]:
    """Establishes connection to the mainframe.

    Args:
        ip_address: IP address of the mainframe.
        port_num: Mainframe port number.

    Returns:
        Integer value representing connection status code.
    """

    if not fieldbus or not fieldbus.ipAddress:
        return GHSReturnValue["NullPtrArgument"]
    if (fieldbus.conHandle.get_num_of_connections() > fieldbus.conHandle.MAX_CONNECTIONS
        or fieldbus.conHandle.connection_count == 0):
        return GHSReturnValue["InvalidHandle"]
    if not fieldbus.conHandle.sock:
        return GHSReturnValue["NoConnection"]

    msg = fieldbus.conHandle.connection_read(size)
    msg_size = len(msg)
    if msg_size != size:
        return GHSReturnValue["NOK"]

    return [GHSReturnValue["OK"], msg]



def read_next_snapshot(
    fieldbus_handle: FieldBus,
    call_type: str | int
) -> tuple[str, float | None, float | None, int | None]:
    """Retrieves the next snapshot in the buffer.

    * The timestamp is grid aligned - as specified by the 'updateRate' argument
    of the GHSInitiateFieldBusDataTransfer() method.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       String value representing request status.
    """

    if not call_type:
        return "NullPtrArgument", None, None, None

    if not fieldbus_handle.dataHandle:
        return "FieldBusError_NullFieldBusRingBuffer", None, None, None

    if isinstance(call_type, int) and call_type in GHSFunctionCallType:
        call_type = to_string(call_type, GHSFunctionCallType)
    elif (
        isinstance(call_type, int)
        and call_type in GHSFunctionCallType.values()
    ):
        pass

    if (not fieldbus_handle.dataHandle.ring_buffer_get_size() and call_type == "NonBlockingCall"):
        timestamp = fieldbus_handle.lastPacket.timeStamp
        values = fieldbus_handle.lastPacket.fValues
        overrun = 0
    else:
        tuple = fieldbus_handle.dataHandle.get_data()
        timestamp = tuple[0]
        values = tuple[1]
        overrun = tuple[2]
        if overrun:
            fieldbus_handle.dataHandle.overrun = 0

    return (
        "OK",
        timestamp,
        values,
        overrun
    )
