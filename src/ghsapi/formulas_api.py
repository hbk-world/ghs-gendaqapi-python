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

"""Formulas module interface."""

from .connection import ConnectionHandler
from .ghsapi_states import (
    RETURN_KEY,
    GHSChannelType,
    GHSReturnValue,
    from_string,
    to_string,
)

# Functions


def get_number_of_scalars(
    con_handle: ConnectionHandler,
) -> tuple[str, int | None]:
    """Get number of scalar formulas in the Mainframe.
    
    The formulaName is UTF-8 encoded.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and the number of scalars.
    """
    
    response_json = con_handle.send_request_wait_response(
        "GetNumberOfScalars", None
    )

    if ("NumberOfScalars" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["NumberOfScalars"],
    )


def get_scalar_info(
    con_handle: ConnectionHandler,
    scalar_index: int,
) -> str:
    """Get scalar information for a certain scalar index.

     The channel name is UTF-8 encoded.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        scalar_index: The index from the scalar collection to identify
        target scalar to get info from.

    Returns:
       Tuple with status and the scalar name, value & unit.
    """

    if not scalar_index:
        return "NullPtrArgument"

    channel_name_dict = {
        "ScalarIndex": scalar_index,
    }

    response_json = con_handle.send_request_wait_response(
        "GetScalarInfo", channel_name_dict
    )

    if (
        not any(
            key in response_json
            for key in [
                "Name",
                "Value",
                "Unit",
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
        response_json["Name"],
        response_json["Value"],
        response_json["Unit"],
    )


def get_scalar_value(
    con_handle: ConnectionHandler,
    formula_name: str,
) -> tuple[str, float | None]:
    """Determine scalar value from a formula name.
    
    The formulaName is UTF-8 encoded.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        formula_name: The formula name of the scalar to get the value from.

    Returns:
       Tuple with status and the scalar value (in double format).
    """
    
    if not formula_name:
        return "NullPtrArgument", None

    range_dict = {
        "FormulaName": formula_name,
    }
    
    response_json = con_handle.send_request_wait_response(
        "GetScalarValue", range_dict
    )

    if ("Value" not in response_json) or (
        response_json[RETURN_KEY] != GHSReturnValue["OK"]
    ):
        return to_string(response_json[RETURN_KEY], GHSReturnValue), None

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        response_json["Value"],
    )


def set_scalar_value(
    con_handle: ConnectionHandler,
    formula_name: str,
    scalar_value: float,
) -> str:
    """Set a scalar value by formula name.

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.
        formula_name: The formula name of the scalar to get the value from.
        scalar_value: The scalar value to be set (in double format).

    Returns:
       String value representing request status.
    """

    if not formula_name or not scalar_value:
        return "NullPtrArgument"

    if not (isinstance(scalar_value, float)):
        return "InvalidDataType"

    span_offset_dict = {
        "FormulaName": formula_name,
        "Value": scalar_value,
    }

    response_json = con_handle.send_request_wait_response(
        "SetScalarValue", span_offset_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)
    
    