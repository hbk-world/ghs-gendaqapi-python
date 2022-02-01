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

"""Connection module interface.

It is used to connect disconnect to the mainframe.
"""

from .connection import ConnectionHandler
from .ghsapi_states import RETURN_KEY, GHSAccess, GHSReturnValue, to_string


def connect(
    con_handle: ConnectionHandler,
    ip_address: int,
    port_num: int,
    client_api_version: int,
) -> str:
    """Interface to connect to the mainframe.

    Args:
        con_handle: A unique identifier per mainframe connection.
        ip_address: Mainframe ip address.
        port_num: Mainframe port number.
        client_api_version: Client supported API version.

    Returns:
        String value representing connect request status.
    """

    if (
        not con_handle
        or not ip_address
        or not port_num
        or not client_api_version
    ):
        return "NullPtrArgument"

    return_var = con_handle.connection_establish(ip_address, port_num)
    if return_var != GHSReturnValue["OK"]:
        return to_string(return_var, GHSReturnValue)

    connect_param_dict = {"ClientAPIVersion": client_api_version}
    response_json = con_handle.send_request_wait_response(
        "Connect", connect_param_dict
    )
    if response_json[RETURN_KEY] != GHSReturnValue["OK"]:
        try:
            if response_json["ServerAPIVersion"] != client_api_version:
                print(
                    f"ServerAPIVersion: {response_json['ServerAPIVersion']} \
                        ClientAPIVersion: {client_api_version}"
                )
        except KeyError:
            pass
        return to_string(response_json[RETURN_KEY], GHSReturnValue)

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_current_access(con_handle: ConnectionHandler) -> str:
    """Interface to get current access permission.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        String representing current access permissions for client.
    """

    response_json = con_handle.send_request_wait_response(
        "GetCurrentAccess", None
    )

    try:
        return to_string(response_json["Access"], GHSAccess)
    except KeyError:
        return to_string(response_json[RETURN_KEY], GHSReturnValue)


def disconnect(con_handle: ConnectionHandler) -> str:
    """Interface to disconnect to the mainframe.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        String value representing disconnect request status.
    """

    response_json = con_handle.send_request_wait_response("Disconnect", None)
    return to_string(response_json[RETURN_KEY], GHSReturnValue)
