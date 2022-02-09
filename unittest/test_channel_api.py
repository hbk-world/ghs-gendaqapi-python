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

"""Channel API unit test."""

import os
import sys
import unittest
from unittest.mock import patch

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(os.path.join(parentdir, "src"))

from ghsapi import channel_api, connection, ghsapi_states


class TestChannelAPI(unittest.TestCase):
    """Channel API unit test."""

    con_handle = connection.ConnectionHandler()
    GHSReturnValue = ghsapi_states.GHSReturnValue
    RETURN_KEY = ghsapi_states.RETURN_KEY

    def setUp(self):
        # run at start of test file
        pass

    def test_get_channel_type(self):
        """Test get_channel_type api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "ChannelType": 1,
                }
                self.assertEqual(
                    channel_api.get_channel_type(self.con_handle, "A", 1),
                    (
                        "OK",
                        "Analog",
                    ),
                    "get_channel_type success response test failed.",
                )

    def test_get_channel_type_neg(self):
        """Test get_channel_type api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "ChannelType": 1,
                }
                self.assertEqual(
                    channel_api.get_channel_type(self.con_handle, "A", 1),
                    ("NOK", None),
                    "get_channel_type failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_channel_type(self.con_handle, "A", 1),
                    ("NOK", None),
                    "get_channel_type failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_channel_type(self.con_handle, "A", 1),
                    ("OK", None),
                    "get_channel_type failure response test failed.",
                )

    def test_get_channel_type_null_args(self):
        """Test get_channel_type api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_channel_type(self.con_handle, None, None),
            ("NullPtrArgument", None),
            "get_channel_type null argument check failed.",
        )

    def test_get_channel_name(self):
        """Test get_channel_name api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "ChannelName": "NewChannelName",
                }
                self.assertEqual(
                    channel_api.get_channel_name(self.con_handle, "A", 1),
                    (
                        "OK",
                        "NewChannelName",
                    ),
                    "get_channel_name success response test failed.",
                )

    def test_get_channel_name_neg(self):
        """Test get_channel_name api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "ChannelName": "NewChannelName",
                }
                self.assertEqual(
                    channel_api.get_channel_name(self.con_handle, "A", 1),
                    ("NOK", None),
                    "get_channel_name failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_channel_name(self.con_handle, "A", 1),
                    ("NOK", None),
                    "get_channel_name failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_channel_name(self.con_handle, "A", 1),
                    ("OK", None),
                    "get_channel_name failure response test failed.",
                )

    def test_get_channel_name_null_args(self):
        """Test get_channel_name api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_channel_name(self.con_handle, None, None),
            ("NullPtrArgument", None),
            "get_channel_name null argument check failed.",
        )

    def test_set_channel_name(self):
        """Test set_channel_name api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.set_channel_name(
                        self.con_handle, "A", 1, "NewChannelName"
                    ),
                    "OK",
                    "set_channel_name success response test failed.",
                )

    def test_set_channel_name_null_args(self):
        """Test set_channel_name api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_channel_name(self.con_handle, None, None, None),
            "NullPtrArgument",
            "set_channel_name null argument check failed.",
        )

    def test_get_channel_storage_enabled(self):
        """Test get_channel_storage_enabled api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "Enabled": 1,
                }
                self.assertEqual(
                    channel_api.get_channel_storage_enabled(
                        self.con_handle, "A", 1
                    ),
                    (
                        "OK",
                        "Enable",
                    ),
                    "get_channel_storage_enabled success response test failed.",
                )

    def test_get_channel_storage_enabled_neg(self):
        """Test get_channel_storage_enabled api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "Enabled": 1,
                }
                self.assertEqual(
                    channel_api.get_channel_storage_enabled(
                        self.con_handle, "A", 1
                    ),
                    ("NOK", None),
                    "get_channel_storage_enabled failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_channel_storage_enabled(
                        self.con_handle, "A", 1
                    ),
                    ("NOK", None),
                    "get_channel_storage_enabled failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_channel_storage_enabled(
                        self.con_handle, "A", 1
                    ),
                    ("OK", None),
                    "get_channel_storage_enabled failure response test failed.",
                )

    def test_get_channel_storage_enabled_null_args(self):
        """Test get_channel_storage_enabled api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_channel_storage_enabled(
                self.con_handle, None, None
            ),
            ("NullPtrArgument", None),
            "get_channel_storage_enabled null argument check failed.",
        )

    def test_set_channel_storage_enabled(self):
        """Test set_channel_storage_enabled api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.set_channel_storage_enabled(
                        self.con_handle, "A", 1, "Enable"
                    ),
                    "OK",
                    "set_channel_storage_enabled success response test failed.",
                )

    def test_set_channel_storage_enabled_null_args(self):
        """Test set_channel_storage_enabled api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_channel_storage_enabled(
                self.con_handle, None, None, None
            ),
            "NullPtrArgument",
            "set_channel_storage_enabled null argument check failed.",
        )

    def test_set_channel_storage_enabled_invalid_args(self):
        """Test set_channel_storage_enabled api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_channel_storage_enabled(
                self.con_handle, "A", 1, "On"
            ),
            "InvalidDataType",
            "set_channel_storage_enabled invalid argument check failed.",
        )

    def test_cmd_zeroing(self):
        """Test cmd_zeroing api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.cmd_zeroing(self.con_handle, "A", 1, "Enable"),
                    "OK",
                    "cmd_zeroing success response test failed.",
                )

    def test_cmd_zeroing_null_args(self):
        """Test cmd_zeroing api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.cmd_zeroing(self.con_handle, None, None, None),
            "NullPtrArgument",
            "cmd_zeroing null argument check failed.",
        )

    def test_cmd_zeroing_invalid_args(self):
        """Test cmd_zeroing api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.cmd_zeroing(self.con_handle, "A", 1, "Zero"),
            "InvalidDataType",
            "cmd_zeroing invalid argument check failed.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Channel API Unittest Report",
            report_title="Channel API Unittest Report",
        )
    )
