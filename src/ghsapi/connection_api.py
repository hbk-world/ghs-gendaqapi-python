"""Connection module interface.

It is used to connect disconnect to the mainframe.
"""

from .ghsapi_states import GHSReturnValue, GHSAccess, RETURN_KEY, to_string


def connect(con_handle, ip_address, port_num, client_api_version):
    """Interface to connect to the mainframe.

    Args:
        con_handle: A unique identifier per mainframe connection.
        ip_address: Mainframe ip address.
        port_num: Mainframe port number.
        client_api_version: Client supported API version.

    Returns:
        An String value representing connect request status.
    """

    if not con_handle or not ip_address or not port_num or not client_api_version:
        return "NullPtrArgument"

    return_var = con_handle.connection_establish(ip_address, port_num)
    if return_var != GHSReturnValue["OK"]:
        return to_string(return_var, GHSReturnValue)

    connect_param_dict = {"ClientAPIVersion": client_api_version}
    response_json = con_handle.send_request_wait_response("Connect", connect_param_dict)
    if response_json[RETURN_KEY] != GHSReturnValue["OK"]:
        return to_string(response_json[RETURN_KEY], GHSReturnValue)

    if response_json["ServerAPIVersion"] != client_api_version:
        print(
            f"ServerAPIVersion : {response_json['ServerAPIVersion']}\
                ClientAPIVersion: {client_api_version}"
        )
        return to_string(GHSReturnValue["APIMismatch"], GHSReturnValue)

    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_current_access(con_handle):
    """Interface to get current access permission.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        An String representing current access permissions for client.
    """

    response_json = con_handle.send_request_wait_response("GetCurrentAccess", 0)

    try:
        return to_string(response_json["Access"], GHSAccess)
    except KeyError:
        return to_string(response_json[RETURN_KEY], GHSReturnValue)


def disconnect(con_handle):
    """Interface to disconnect to the mainframe.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        An String value representing disconnect request status.
    """

    response_json = con_handle.send_request_wait_response("Disconnect", 0)
    return to_string(response_json[RETURN_KEY], GHSReturnValue)
