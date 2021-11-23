"""``Request`` ``Response`` utilities for JSON-RPC client.

Implementation of request and response utility function for JSON-RPC
client APIs.
"""

import json
from collections import OrderedDict

from .ghsapi_states import RETURN_KEY, GHSReturnValue


def json_rpc_create_request(
    request_id: int, method_name: str, method_param: dict | None
) -> bytes:
    """``Create`` ``JSON-RPC`` client request"""

    if method_param:
        json_obj = OrderedDict(
            [
                ("jsonrpc", "2.0"),
                ("method", method_name),
                ("params", method_param),
                ("id", request_id),
            ]
        )
    else:
        json_obj = OrderedDict(
            [
                ("jsonrpc", "2.0"),
                ("method", method_name),
                ("id", request_id),
            ]
        )
    request_json = json.dumps(json_obj, separators=(",", ":")) + "\0"
    return request_json.encode("utf-8")


def json_rpc_check_errors(request_id: int, response_dict: dict) -> int:
    """Check for errors in JSON-RPC response"""

    if int(response_dict["id"]) != request_id:
        return GHSReturnValue["NOK"]
    # If retreivedRequestID is null means some critical error was
    # received by the client
    if response_dict["id"] == "null":
        try:
            # if response_dict has key "error"
            # Depending on the code the message sent to application can
            # differ
            error_code = response_dict["error"]["code"]
            if error_code == -32700:
                return GHSReturnValue["InvalidJSONFormat"]
            return GHSReturnValue["UnkownErrorMessage"]
        except KeyError:
            return GHSReturnValue["NOK"]
    # Determine how to handle the message depending on what's in it
    try:
        # if response_dict.has_key("error"):
        error_code = response_dict["error"]["code"]
        if error_code == -32601:
            return GHSReturnValue["MethodNotFound"]
        return GHSReturnValue["UnkownErrorMessage"]
    except KeyError:
        return GHSReturnValue["OK"]


def json_rpc_parse_response(
    request_id: int, response_json: bytes | None
) -> dict:
    """``Parse`` ``JSON-RPC`` response"""

    parsed_json = json.loads(response_json[:-1])
    # Check if retrevied JSON has any error code in it
    return_var = json_rpc_check_errors(request_id, parsed_json)
    if return_var != GHSReturnValue["OK"]:
        return {RETURN_KEY: return_var}
    try:
        # if parsed_json has key "result"
        # A result number in the response MUST be a GHSReturnValue
        # integer, return that
        if isinstance(parsed_json["result"], int):
            return {RETURN_KEY: parsed_json["result"]}
        # A result object in the response MUST have a GHSReturnValue
        # named parameter, return that
        try:
            # if parsed_json["result"] has key "GHSReturnValue"
            return parsed_json["result"]
        # Invalid JSON-RPC response
        except KeyError:
            return {RETURN_KEY: GHSReturnValue["NOK"]}
    # Invalid JSON-RPC response
    except KeyError:
        return {RETURN_KEY: GHSReturnValue["NOK"]}
