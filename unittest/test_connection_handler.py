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

"""Connection Handler unit test."""

import os
import sys
import unittest
from struct import pack
from unittest.mock import patch

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(os.path.join(parentdir, "src"))

from ghsapi import connection, ghsapi_states, json_rpc

IP_ADDRESS = "localhost"
PORT_NO = 8006


class TestConnectionHandler(unittest.TestCase):
    """Connection Handler unit test."""

    con_handle = connection.ConnectionHandler()
    GHSReturnValue = ghsapi_states.GHSReturnValue
    RETURN_KEY = ghsapi_states.RETURN_KEY

    def setUp(self):
        # run at start of test file
        self.con_handle.connection_count = 0
        self.con_handle.request_id = 0
        self.con_handle.sock = 0
        self.con_handle.ip_address = 0

    def test_null_args(self):
        """Test null arguments."""

        self.assertEqual(
            self.con_handle.connection_establish(None, None),
            self.GHSReturnValue["NullPtrArgument"],
            "Null argument check failed.",
        )

        self.assertEqual(
            self.con_handle.connection_establish("localhost", None),
            self.GHSReturnValue["NullPtrArgument"],
            "Null argument check failed.",
        )

        self.assertEqual(
            self.con_handle.connection_establish(None, 8006),
            self.GHSReturnValue["NullPtrArgument"],
            "Null argument check failed.",
        )

        return_val = self.con_handle.send_request_wait_response(None, None)
        self.assertEqual(
            return_val[self.RETURN_KEY],
            self.GHSReturnValue["NullPtrArgument"],
            "Null argument check failed.",
        )

    def test_connection_count(self):
        """Test connection counter"""

        with patch("test_connection_handler.connection.socket.socket"):
            self.assertEqual(
                self.con_handle.connection_count,
                0,
                "Invalid initial connection count.",
            )
            self.con_handle.connection_establish(IP_ADDRESS, PORT_NO)
            self.assertEqual(
                self.con_handle.connection_count,
                1,
                "Connection counter failed.",
            )

    def test_invalid_num_of_connections(self):
        """Test invalid number of connections"""

        self.con_handle.connection_count = 31
        self.assertEqual(
            self.con_handle.connection_establish(IP_ADDRESS, PORT_NO),
            self.GHSReturnValue["ConnectionFailed"],
            "Max number of connection check failed.",
        )

    def test_socket_connect(self):
        """Test senarios of socket connect call mocking socket"""

        self.assertEqual(
            self.con_handle.connection_establish(IP_ADDRESS, PORT_NO),
            self.GHSReturnValue["NoConnection"],
            "Socket connect with NoConnection senario failed.",
        )

        with patch("test_connection_handler.connection.socket.socket"):
            self.assertEqual(
                self.con_handle.connection_establish(IP_ADDRESS, PORT_NO),
                self.GHSReturnValue["OK"],
                "Socket connect failed.",
            )
            self.assertEqual(
                self.con_handle.connection_establish(None, None),
                self.GHSReturnValue["NullPtrArgument"],
                "Socket connect with null args failed.",
            )

    def test_socket_write(self):
        """Test senarios of socket write mocking socket"""

        self.con_handle.request_id += 1
        method_name = "Connect"
        method_param = {"ClientAPIVersion": 5}
        request_json = json_rpc.json_rpc_create_request(
            self.con_handle.request_id, method_name, method_param
        )
        write_len = len(request_json)
        header_sx = pack("!I", write_len) + pack(
            "!I", self.con_handle.api_version_header
        )

        with patch(
            "test_connection_handler.connection.socket.socket.send"
        ) as mock_send:
            self.con_handle.connection_establish(IP_ADDRESS, PORT_NO)

            mock_send.return_value = len(header_sx)
            self.assertEqual(
                self.con_handle.connection_write(header_sx, len(header_sx)),
                len(header_sx),
                "Socket write with header failed.",
            )

            mock_send.return_value = write_len
            self.assertEqual(
                self.con_handle.connection_write(request_json, write_len),
                write_len,
                "Socket write with request json failed.",
            )

    def test_socket_read(self):
        """Test senarios of socket read mocking socket"""

        self.con_handle.request_id += 1

        with patch(
            "test_connection_handler.connection.socket.socket.recv"
        ) as mock_recv:
            self.con_handle.connection_establish(IP_ADDRESS, PORT_NO)

            mock_recv.return_value = b"testdata"
            size = 8
            self.assertEqual(
                len(self.con_handle.connection_read(size)),
                size,
                "Socket read failed.",
            )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Connection Handler Unittest Report",
            report_title="Connection Handler Unittest Report",
        )
    )
