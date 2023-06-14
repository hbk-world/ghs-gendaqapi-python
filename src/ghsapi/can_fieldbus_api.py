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
    GHSEnableDisable,
    from_string,
    to_string,
)


def get_can_acq_control(
    con_handle: ConnectionHandler
) -> tuple[str, str | None, int | None, int | None]:
    """Get the current setup of CAN acquisition control

     Read - This method can be called by multiple connected clients at
     same time.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       Tuple with status and:
        Flag to indicate if feature is on
        The one-based index that specifies which CAN controller is used
        Message ID of the CAN acquisition control
    """

    response_json = con_handle.send_request_wait_response(
        "GetCANAcqControl", None
    )

    if (
        not any(
            key in response_json
            for key in [
                "Enable",
                "MsgID",
                "BusID"
            ]
        )
    ) or (response_json[RETURN_KEY] != GHSReturnValue["OK"]):
        return (
            to_string(response_json[RETURN_KEY], GHSReturnValue),
            None,
            None,
            None
        )

    return (
        to_string(response_json[RETURN_KEY], GHSReturnValue),
        to_string(response_json["Enable"], GHSEnableDisable),
        response_json["MsgID"],
        response_json["BusID"]
    )


def set_can_acq_control(
    con_handle: ConnectionHandler,
    enabled: str,
    bus_id: int,
    msg_id: int
) -> str:
    """Set up CAN acquisition control.
    
    * The system needs to be idle before calling this function.

    This method will only process requests from the connected client
    with the most privileges order (Privileges order: 1- Perception,
    2- GenDaq, 3- Other)

    Args:
        con_handle: A unique identifier per mainframe connection.
        enabled: Flag to indicate if feature is on
        bus_id: The one-based index that specifies which CAN controller to use
        msg_id: Message ID of the CAN acquisition control

    Returns:
       String value representing request status.
    """

    if not enabled or not bus_id or not msg_id:
        return "NullPtrArgument"

    if isinstance(enabled, str) and enabled in GHSEnableDisable:
        enabled = from_string(enabled, GHSEnableDisable)

    elif isinstance(enabled, int) and enabled in GHSEnableDisable.values():
        pass

    else:
        return "InvalidDataType"

    dict = {
        "Enable": enabled,
        "BusID": bus_id,
        "MsgID": msg_id
    }

    response_json = con_handle.send_request_wait_response(
        "SetCANAcqControl", dict
    )

    return (to_string(response_json[RETURN_KEY], GHSReturnValue))