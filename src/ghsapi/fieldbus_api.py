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

"""Fieldbus module interface."""

from .connection import ConnectionHandler
from .ghsapi_states import (
    RETURN_KEY,
    GHSReturnValue,
    to_string,
)

    
FLOAT_PRECISION = 3


# Functions
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

    if data_index < 0 or data_index is None:
        return "NullPtrArgument", None, None

    fieldbus_type_dict = {
        "DataIndex": data_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetFieldBusDataNameAndUnit", fieldbus_type_dict
    )

    if ("DataName" not in response_json) or ("DataUnit" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None, None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["DataName"],
        response_json["DataUnit"]
    )


def get_fieldbus_data_count(
    con_handle: ConnectionHandler
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

def get_fieldbus_request_snapshot(
    con_handle: ConnectionHandler,
    data_count: int,
) -> tuple[str, list[float] | None, int | None, list[float] | None]:
    """ Request a single snapshot of the field bus data.
    
    *In this case the timestamp received is not grid aligned.
    
    *If the system is not acquiring the method returns an error code: SystemNotRecording
    
    *In case of no formulas you get the error return code back: FieldBusError_NotConfigured
    
    *If the field bus is already enabled then this method is not allowed. 
    An error return code is returned: FieldBusError_FieldBusAlready_Enabled
    
    *Read - This method can be called by multiple connected clients at same
    time.*

    Args:
        con_handle: A unique identifier per mainframe connection.
        data_index: Zero-based index of the data value.
    
    Returns:
       Tuple with status, timestamp, total number of fieldbus channels and the fieldbus data.
    """

    if data_count < 0 or data_count is None:
        return "NullPtrArgument", None, None, None

    response_json = con_handle.send_request_wait_response(
        "RequestSnapshot", None
    )

    if ("DataCount" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None, None, None

    if (data_count != response_json["DataCount"]):
        return "FieldBusError_BufferSizeInvalid", None, None, None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        round(response_json["TimeStamp"], FLOAT_PRECISION),
        response_json["DataCount"],
        [round(channel_data, FLOAT_PRECISION) for channel_data in response_json["Data"]]
    )
