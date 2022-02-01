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

"""Implementaion of Connection module."""

import errno
import socket
from struct import pack, unpack

from . import json_rpc
from .ghsapi_states import RETURN_KEY, GHSReturnValue

MAX_CONNECTIONS = 30


class ConnectionHandler:
    """A unique identifier per mainframe connection.

    It is used by all API calls to distinguish between mainframes.

    Attributes:
        connection_count: An integer count of all connections.
        api_version_header: Client API header version.
        request_id: Client request id
        sock: Socket object
        ip_address: Mainframe ip address
    """

    connection_count = 0
    api_version_header = 1195638785

    def __init__(self):
        self.request_id = 0
        self.sock = 0
        self.ip_address = 0

    def get_num_of_connections(self) -> int:
        """Get count of all connections."""

        return self.connection_count

    def get_ip_address(self) -> int:
        """Get ip address of mainframe."""

        return self.ip_address

    def connection_establish(self, ip_address: int, port_num: int) -> int:
        """Establishes connection to the mainframe.

        Args:
            ip_address: IP address of the mainframe.
            port_num: Mainframe port number.

        Returns:
            Integer value representing connection status code.
        """

        if not ip_address or not port_num:
            return GHSReturnValue["NullPtrArgument"]
        if self.get_num_of_connections() > MAX_CONNECTIONS:
            return GHSReturnValue["ConnectionFailed"]

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            return GHSReturnValue["ConnectionFailed"]
        except RuntimeError:
            return GHSReturnValue["NOK"]

        try:
            self.sock.connect((ip_address, port_num))
        except socket.gaierror:
            return GHSReturnValue["ConnectionFailed"]
        except socket.error:
            return GHSReturnValue["NoConnection"]
        except RuntimeError:
            return GHSReturnValue["NOK"]

        self.ip_address = ip_address
        self.connection_count += 1
        return GHSReturnValue["OK"]

    def send_request_wait_response(
        self, method_name: str, method_param: dict | None
    ) -> dict:
        """Sends request to the mainframe.

        Args:
            method_name: Request method name .
            method_param: Request method parameter.

        Returns:
            Dict representing response from the mainframe.
        """

        if not method_name:
            return {RETURN_KEY: GHSReturnValue["NullPtrArgument"]}

        self.request_id += 1
        request_json = json_rpc.json_rpc_create_request(
            self.request_id, method_name, method_param
        )
        write_len = len(request_json)
        header_sx = pack("!I", write_len) + pack("!I", self.api_version_header)

        try:
            if self.connection_write(header_sx, len(header_sx)) != len(
                header_sx
            ):
                return {RETURN_KEY: GHSReturnValue["NOK"]}
            if self.connection_write(request_json, write_len) != write_len:
                return {RETURN_KEY: GHSReturnValue["NOK"]}
        except OSError:
            return {RETURN_KEY: GHSReturnValue["NoConnection"]}
        except RuntimeError:
            return {RETURN_KEY: GHSReturnValue["NOK"]}
        except Exception:
            return {RETURN_KEY: GHSReturnValue["NoConnection"]}

        header_rx_size = 8
        header_rx = self.connection_read(header_rx_size)
        if header_rx_size != len(header_rx):
            return {RETURN_KEY: GHSReturnValue["NOK"]}

        header_rx_packet_header = unpack(">II", header_rx)
        if header_rx_packet_header[1] != self.api_version_header:
            return {RETURN_KEY: GHSReturnValue["NOK"]}

        response_json = self.connection_read(header_rx_packet_header[0])
        return json_rpc.json_rpc_parse_response(self.request_id, response_json)

    def connection_read(self, length: int) -> bytes:
        """Read message in bytes.

        Args:
            length: Message length.

        Returns:
            Bytes of message read.

        Raises:
            OSError: When socket not connected
            RuntimeError: When socket connection broken
        """

        message = b""
        while len(message) < length:
            try:
                packet = self.sock.recv(length - len(message))
                if not packet:
                    return None
                message += packet
            except socket.error as socket_error:
                err = socket_error.args[0]
                if err in (errno.EAGAIN, errno.EWOULDBLOCK):
                    print("connection_read: No data available")
                # return None
                # print("connection_read: No data available")
                # return None
        return message

    def connection_write(self, message: bytes, length: int) -> int:
        """Writes message in bytes.

        Args:
            message: Message to write.
            length: Message length.

        Returns:
            Integer representing bytes written.

        Raises:
            OSError: When socket not connected
            RuntimeError: When socket connection broken
        """

        written_bytes = 0
        sent_bytes = 0

        while written_bytes < length:
            try:
                sent_bytes = self.sock.send(message[written_bytes:])
            except AttributeError as no_socket:
                raise OSError("Socket not Connected") from no_socket
            except socket.gaierror as no_socket:
                raise OSError("Socket not Connected") from no_socket
            except RuntimeError as un_specific_error:
                raise RuntimeError from un_specific_error
            except Exception as any_exception:
                raise Exception from any_exception
            if sent_bytes == 0:
                raise RuntimeError("Socket Connection Broken")
            written_bytes = written_bytes + sent_bytes
            sent_bytes = 0

        return written_bytes
