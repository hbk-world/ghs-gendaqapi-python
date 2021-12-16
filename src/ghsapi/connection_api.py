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
