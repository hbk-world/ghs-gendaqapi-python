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

"""Manage mainframe settings module interface."""

from .connection import ConnectionHandler
from .ghsapi_states import RETURN_KEY, GHSReturnValue, to_string


def apply_persisted_settings(con_handle: ConnectionHandler) -> str:
    """A mainframe might contain persisted settings (being applied upon
    boot). This method re-applies these settings. In Perception this
    maps on the 'Configured boot' feature.

    The system needs to be idle before calling this function.
    This function overwrites any previously set settings and / or
    persisted settings.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       String value representing request status.
    """

    response_json = con_handle.send_request_wait_response(
        "ApplyPersistedSettings", None
    )
    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def persist_current_settings(con_handle: ConnectionHandler) -> str:
    """Persists the current mainframe settings.

    The persisted mainframe settings are applied upon a mainframe boot.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
       String value representing request status.
    """

    response_json = con_handle.send_request_wait_response(
        "PersistCurrentSettings", None
    )
    return to_string(response_json[RETURN_KEY], GHSReturnValue)


def get_current_settings(
    con_handle: ConnectionHandler,
) -> tuple[str, bytes | None, int | None]:
    """Retrieves the current mainframe settings as a blob.

    As this blob can be of variable size, it is upon the caller to
    ensure reading the correct amount of memory.
    Memory for this blob is allocated by the API.

    Args:
        con_handle: A unique identifier per mainframe connection.

    Returns:
        Tuple with status, base name and index of the recording file.
    """

    response_json = con_handle.send_request_wait_response(
        "GetCurrentSettings", None
    )

    if (
        not any(
            key in response_json
            for key in [
                "Size",
                "Blob",
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
        response_json["Blob"],
        response_json["Size"],
    )


def set_current_settings(
    con_handle: ConnectionHandler, blob: bytes, blob_size: int
) -> str:
    """Applies the mainframe settings contained in the input argument.

    Note that this function overwrites any previously set settings and
    / or applied setup.

    The system needs to be idle before calling this function.

    Args:
        con_handle: A unique identifier per mainframe connection.
        blob: Settings blob.
        blob_size: Size of the settings blob.

    Returns:
        String value representing request status.
    """

    if not blob or not blob_size:
        return "NullPtrArgument"

    current_settings_dict = {"Blob": blob, "Size": blob_size}
    response_json = con_handle.send_request_wait_response(
        "SetCurrentSettings", current_settings_dict
    )

    return to_string(response_json[RETURN_KEY], GHSReturnValue)
