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

    # Functions
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
                    channel_api.get_channel_name(self.con_handle, "A", 1, "Analog"),
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
                    channel_api.get_channel_name(self.con_handle, "A", 1, "Analog"),
                    ("NOK", None),
                    "get_channel_name failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_channel_name(self.con_handle, "A", 1 , "Analog"),
                    ("NOK", None),
                    "get_channel_name failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_channel_name(self.con_handle, "A", 1, "Analog"),
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
            channel_api.get_channel_name(self.con_handle, None, None, None),
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
                        self.con_handle, "A", 1, "Analog","NewChannelName"
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
            channel_api.set_channel_name(self.con_handle, None, None, None, None),
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
                        self.con_handle, "A", 1, "Analog"
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
                        self.con_handle, "A", 1, "Analog"
                    ),
                    ("NOK", None),
                    "get_channel_storage_enabled failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_channel_storage_enabled(
                        self.con_handle, "A", 1, "Analog"
                    ),
                    ("NOK", None),
                    "get_channel_storage_enabled failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_channel_storage_enabled(
                        self.con_handle, "A", 1, "Analog"
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
                self.con_handle, None, None, None
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
                        self.con_handle, "A", 1, "Analog", "Enable"
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
                self.con_handle, None, None, None, None
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
                self.con_handle, "A", 1, "Analog", "On"
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
                    channel_api.cmd_zeroing(self.con_handle, "A", 1, "Analog", "Enable"),
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
            channel_api.cmd_zeroing(self.con_handle, None, None, None, None),
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
            channel_api.cmd_zeroing(self.con_handle, "A", 1, "Analog", "Zero"),
            "InvalidDataType",
            "cmd_zeroing invalid argument check failed.",
        )

    # Analog module
    def test_get_trigger_settings(self):
        """Test get_trigger_settings api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "TriggerMode": 2,
                    "PrimaryLevel": 10.0,
                    "SecondaryLevel": 20.0,
                    "Hysteresis": 30.0,
                    "Direction": 0,
                }
                self.assertEqual(
                    channel_api.get_trigger_settings(self.con_handle, "A", 1),
                    (
                        "OK",
                        "Dual",
                        10.0,
                        20.0,
                        30.0,
                        "RisingEdge",
                    ),
                    "get_trigger_settings success response test failed.",
                )

    def test_get_trigger_settings_neg(self):
        """Test get_trigger_settings api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "TriggerMode": 2,
                    "PrimaryLevel": 10.0,
                    "SecondaryLevel": 20.0,
                    "Hysteresis": 30.0,
                    "Direction": 0,
                }
                self.assertEqual(
                    channel_api.get_trigger_settings(self.con_handle, "A", 1),
                    ("NOK", None, None, None, None, None),
                    "get_trigger_settings failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_trigger_settings(self.con_handle, "A", 1),
                    ("NOK", None, None, None, None, None),
                    "get_trigger_settings failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_trigger_settings(self.con_handle, "A", 1),
                    ("OK", None, None, None, None, None),
                    "get_trigger_settings failure response test failed.",
                )

    def test_get_trigger_settings_null_args(self):
        """Test get_trigger_settings api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_trigger_settings(self.con_handle, None, None),
            ("NullPtrArgument", None, None, None, None, None),
            "get_trigger_settings null argument check failed.",
        )

    def test_set_trigger_settings(self):
        """Test set_trigger_settings api with success response"""

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
                    channel_api.set_trigger_settings(
                        self.con_handle,
                        "A",
                        1,
                        "Dual",
                        10,
                        20,
                        30,
                        "RisingEdge",
                    ),
                    "OK",
                    "set_trigger_settings success response test failed.",
                )

    def test_set_trigger_settings_null_args(self):
        """Test set_trigger_settings api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_trigger_settings(
                self.con_handle, None, None, None, None, None, None, None
            ),
            "NullPtrArgument",
            "set_trigger_settings null argument check failed.",
        )

    def test_set_trigger_settings_invalid_args(self):
        """Test set_trigger_settings api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_trigger_settings(
                self.con_handle, "A", 1, "Two", 10, 20, 30, "RisingEdge"
            ),
            "InvalidDataType",
            "set_trigger_settings invalid argument check failed.",
        )
        self.assertEqual(
            channel_api.set_trigger_settings(
                self.con_handle, "A", 1, "Dual", 10, 20, 30, "Rising"
            ),
            "InvalidDataType",
            "set_trigger_settings invalid argument check failed.",
        )

    def test_get_signal_coupling(self):
        """Test get_signal_coupling api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "SignalCoupling": 1,
                }
                self.assertEqual(
                    channel_api.get_signal_coupling(self.con_handle, "A", 1),
                    (
                        "OK",
                        "DC",
                    ),
                    "get_signal_coupling success response test failed.",
                )

    def test_get_signal_coupling_neg(self):
        """Test get_signal_coupling api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "SignalCoupling": 1,
                }
                self.assertEqual(
                    channel_api.get_signal_coupling(self.con_handle, "A", 1),
                    ("NOK", None),
                    "get_signal_coupling failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_signal_coupling(self.con_handle, "A", 1),
                    ("NOK", None),
                    "get_signal_coupling failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_signal_coupling(self.con_handle, "A", 1),
                    ("OK", None),
                    "get_signal_coupling failure response test failed.",
                )

    def test_get_signal_coupling_null_args(self):
        """Test get_signal_coupling api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_signal_coupling(self.con_handle, None, None),
            ("NullPtrArgument", None),
            "get_signal_coupling null argument check failed.",
        )

    def test_set_signal_coupling(self):
        """Test set_signal_coupling api with success response"""

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
                    channel_api.set_signal_coupling(
                        self.con_handle, "A", 1, "DC"
                    ),
                    "OK",
                    "set_signal_coupling success response test failed.",
                )

    def test_set_signal_coupling_null_args(self):
        """Test set_signal_coupling api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_signal_coupling(self.con_handle, None, None, None),
            "NullPtrArgument",
            "set_signal_coupling null argument check failed.",
        )

    def test_set_signal_coupling_invalid_args(self):
        """Test set_signal_coupling api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_signal_coupling(self.con_handle, "A", 1, "PC"),
            "InvalidDataType",
            "set_signal_coupling invalid argument check failed.",
        )

    def test_get_input_coupling(self):
        """Test get_input_coupling api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "InputCoupling": 3,
                }
                self.assertEqual(
                    channel_api.get_input_coupling(self.con_handle, "A", 1),
                    (
                        "OK",
                        "Current",
                    ),
                    "get_input_coupling success response test failed.",
                )

    def test_get_input_coupling_neg(self):
        """Test get_input_coupling api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "InputCoupling": 3,
                }
                self.assertEqual(
                    channel_api.get_input_coupling(self.con_handle, "A", 1),
                    ("NOK", None),
                    "get_input_coupling failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_input_coupling(self.con_handle, "A", 1),
                    ("NOK", None),
                    "get_input_coupling failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_input_coupling(self.con_handle, "A", 1),
                    ("OK", None),
                    "get_input_coupling failure response test failed.",
                )

    def test_get_input_coupling_null_args(self):
        """Test get_input_coupling api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_input_coupling(self.con_handle, None, None),
            ("NullPtrArgument", None),
            "get_input_coupling null argument check failed.",
        )

    def test_set_input_coupling(self):
        """Test set_input_coupling api with success response"""

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
                    channel_api.set_input_coupling(
                        self.con_handle, "A", 1, "Current"
                    ),
                    "OK",
                    "set_input_coupling success response test failed.",
                )

    def test_set_input_coupling_null_args(self):
        """Test set_input_coupling api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_input_coupling(self.con_handle, None, None, None),
            "NullPtrArgument",
            "set_input_coupling null argument check failed.",
        )

    def test_set_input_coupling_invalid_args(self):
        """Test set_input_coupling api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_input_coupling(self.con_handle, "A", 1, "Curr"),
            "InvalidDataType",
            "set_input_coupling invalid argument check failed.",
        )

    def test_get_span_and_offset(self):
        """Test get_span_and_offset api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "Span": 10.0,
                    "Offset": 20.0,
                }
                self.assertEqual(
                    channel_api.get_span_and_offset(self.con_handle, "A", 1),
                    ("OK", 10.0, 20.0),
                    "get_span_and_offset success response test failed.",
                )

    def test_get_span_and_offset_neg(self):
        """Test get_span_and_offset api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "Span": 10.0,
                    "Offset": 20.0,
                }
                self.assertEqual(
                    channel_api.get_span_and_offset(self.con_handle, "A", 1),
                    ("NOK", None, None),
                    "get_span_and_offset failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_span_and_offset(self.con_handle, "A", 1),
                    ("NOK", None, None),
                    "get_span_and_offset failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_span_and_offset(self.con_handle, "A", 1),
                    ("OK", None, None),
                    "get_span_and_offset failure response test failed.",
                )

    def test_get_span_and_offset_null_args(self):
        """Test get_span_and_offset api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_span_and_offset(self.con_handle, None, None),
            ("NullPtrArgument", None, None),
            "get_span_and_offset null argument check failed.",
        )

    def test_set_span_and_offset(self):
        """Test set_span_and_offset api with success response"""

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
                    channel_api.set_span_and_offset(
                        self.con_handle, "A", 1, 10.0, 20.0
                    ),
                    "OK",
                    "set_span_and_offset success response test failed.",
                )

    def test_set_span_and_offset_null_args(self):
        """Test set_span_and_offset api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_span_and_offset(
                self.con_handle, None, None, None, None
            ),
            "NullPtrArgument",
            "set_span_and_offset null argument check failed.",
        )

    def test_set_span_and_offset_invalid_args(self):
        """Test set_span_and_offset api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_span_and_offset(self.con_handle, "A", 1, 10, 20),
            "InvalidDataType",
            "set_span_and_offset invalid argument check failed.",
        )

    def test_get_filter_type_and_frequency(self):
        """Test get_filter_type_and_frequency api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "FilterType": 6,
                    "Frequency": 25.0,
                }
                self.assertEqual(
                    channel_api.get_filter_type_and_frequency(
                        self.con_handle, "A", 1
                    ),
                    ("OK", "Bessel_AA", 25.0),
                    "get_filter_type_and_frequency success response test failed.",
                )

    def test_get_filter_type_and_frequency_neg(self):
        """Test get_filter_type_and_frequency api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "FilterType": 6,
                    "Frequency": 25.0,
                }
                self.assertEqual(
                    channel_api.get_filter_type_and_frequency(
                        self.con_handle, "A", 1
                    ),
                    ("NOK", None, None),
                    "get_filter_type_and_frequency failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_filter_type_and_frequency(
                        self.con_handle, "A", 1
                    ),
                    ("NOK", None, None),
                    "get_filter_type_and_frequency failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_filter_type_and_frequency(
                        self.con_handle, "A", 1
                    ),
                    ("OK", None, None),
                    "get_filter_type_and_frequency failure response test failed.",
                )

    def test_get_filter_type_and_frequency_null_args(self):
        """Test get_filter_type_and_frequency api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_filter_type_and_frequency(
                self.con_handle, None, None
            ),
            ("NullPtrArgument", None, None),
            "get_filter_type_and_frequency null argument check failed.",
        )

    def test_set_filter_type_and_frequency(self):
        """Test set_filter_type_and_frequency api with success response"""

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
                    channel_api.set_filter_type_and_frequency(
                        self.con_handle, "A", 1, "Bessel_AA", 25.0
                    ),
                    "OK",
                    "set_filter_type_and_frequency success response test failed.",
                )

    def test_set_filter_type_and_frequency_null_args(self):
        """Test set_filter_type_and_frequency api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_filter_type_and_frequency(
                self.con_handle, None, None, None, None
            ),
            "NullPtrArgument",
            "set_filter_type_and_frequency null argument check failed.",
        )

    def test_set_filter_type_and_frequency_invalid_args(self):
        """Test set_filter_type_and_frequency api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_filter_type_and_frequency(
                self.con_handle, "A", 1, "Bessel_AAA", 25.0
            ),
            "InvalidDataType",
            "set_filter_type_and_frequency invalid argument check failed.",
        )
        self.assertEqual(
            channel_api.set_filter_type_and_frequency(
                self.con_handle, "A", 1, "Bessel_AA", 25
            ),
            "InvalidDataType",
            "set_filter_type_and_frequency invalid argument check failed.",
        )

    def test_get_excitation(self):
        """Test get_excitation api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "ExcitationType": 0,
                    "ExcitationValue": 25.0,
                }
                self.assertEqual(
                    channel_api.get_excitation(self.con_handle, "A", 1),
                    ("OK", "Voltage", 25.0),
                    "get_excitation success response test failed.",
                )

    def test_get_excitation_neg(self):
        """Test get_excitation api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "ExcitationType": 0,
                    "ExcitationValue": 25.0,
                }
                self.assertEqual(
                    channel_api.get_excitation(self.con_handle, "A", 1),
                    ("NOK", None, None),
                    "get_excitation failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_excitation(self.con_handle, "A", 1),
                    ("NOK", None, None),
                    "get_excitation failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_excitation(self.con_handle, "A", 1),
                    ("OK", None, None),
                    "get_excitation failure response test failed.",
                )

    def test_get_excitation_null_args(self):
        """Test get_excitation api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_excitation(self.con_handle, None, None),
            ("NullPtrArgument", None, None),
            "get_excitation null argument check failed.",
        )

    def test_set_excitation(self):
        """Test set_excitation api with success response"""

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
                    channel_api.set_excitation(
                        self.con_handle, "A", 1, "Voltage", 25.0
                    ),
                    "OK",
                    "set_excitation success response test failed.",
                )

    def test_set_excitation_null_args(self):
        """Test set_excitation api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_excitation(
                self.con_handle, None, None, None, None
            ),
            "NullPtrArgument",
            "set_excitation null argument check failed.",
        )

    def test_set_excitation_invalid_args(self):
        """Test set_excitation api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_excitation(self.con_handle, "A", 1, "Vol", 25.0),
            "InvalidDataType",
            "set_excitation invalid argument check failed.",
        )
        self.assertEqual(
            channel_api.set_excitation(self.con_handle, "A", 1, "Voltage", 25),
            "InvalidDataType",
            "set_excitation invalid argument check failed.",
        )

    def test_get_amplifier_mode(self):
        """Test get_amplifier_mode api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "AmplifierMode": 0,
                }
                self.assertEqual(
                    channel_api.get_amplifier_mode(self.con_handle, "A", 1),
                    ("OK", "Basic"),
                    "get_amplifier_mode success response test failed.",
                )

    def test_get_amplifier_mode_neg(self):
        """Test get_amplifier_mode api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "AmplifierMode": 0,
                }
                self.assertEqual(
                    channel_api.get_amplifier_mode(self.con_handle, "A", 1),
                    ("NOK", None),
                    "get_amplifier_mode failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_amplifier_mode(self.con_handle, "A", 1),
                    ("NOK", None),
                    "get_amplifier_mode failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_amplifier_mode(self.con_handle, "A", 1),
                    ("OK", None),
                    "get_amplifier_mode failure response test failed.",
                )

    def test_get_amplifier_mode_null_args(self):
        """Test get_amplifier_mode api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_amplifier_mode(self.con_handle, None, None),
            ("NullPtrArgument", None),
            "get_amplifier_mode null argument check failed.",
        )

    def test_set_amplifier_mode(self):
        """Test set_amplifier_mode api with success response"""

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
                    channel_api.set_amplifier_mode(
                        self.con_handle, "A", 1, "Basic"
                    ),
                    "OK",
                    "set_amplifier_mode success response test failed.",
                )

    def test_set_amplifier_mode_null_args(self):
        """Test set_amplifier_mode api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_amplifier_mode(self.con_handle, None, None, None),
            "NullPtrArgument",
            "set_amplifier_mode null argument check failed.",
        )

    def test_set_amplifier_mode_invalid_args(self):
        """Test set_amplifier_mode api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_amplifier_mode(self.con_handle, "A", 1, "Base"),
            "InvalidDataType",
            "set_amplifier_mode invalid argument check failed.",
        )

    def test_get_technical_units(self):
        """Test get_technical_units api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "UnitType": "KGS",
                    "Multiplier": 10.0,
                    "Offset": 20.0,
                }
                self.assertEqual(
                    channel_api.get_technical_units(self.con_handle, "A", 1),
                    ("OK", "KGS", 10.0, 20.0),
                    "get_technical_units success response test failed.",
                )

    def test_get_technical_units_neg(self):
        """Test get_technical_units api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "UnitType": "KGS",
                    "Multiplier": 10.0,
                    "Offset": 20.0,
                }
                self.assertEqual(
                    channel_api.get_technical_units(self.con_handle, "A", 1),
                    ("NOK", None, None, None),
                    "get_technical_units failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_technical_units(self.con_handle, "A", 1),
                    ("NOK", None, None, None),
                    "get_technical_units failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_technical_units(self.con_handle, "A", 1),
                    ("OK", None, None, None),
                    "get_technical_units failure response test failed.",
                )

    def test_get_technical_units_null_args(self):
        """Test get_technical_units api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_technical_units(self.con_handle, None, None),
            ("NullPtrArgument", None, None, None),
            "get_technical_units null argument check failed.",
        )

    def test_set_technical_units(self):
        """Test set_technical_units api with success response"""

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
                    channel_api.set_technical_units(
                        self.con_handle, "A", 1, "KGS", 10.0, 20.0
                    ),
                    "OK",
                    "set_technical_units success response test failed.",
                )

    def test_set_technical_units_null_args(self):
        """Test set_technical_units api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_technical_units(
                self.con_handle, None, None, None, None, None
            ),
            "NullPtrArgument",
            "set_technical_units null argument check failed.",
        )

    def test_set_technical_units_invalid_args(self):
        """Test set_technical_units api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_technical_units(
                self.con_handle, "A", 1, 10, 10.0, 20.0
            ),
            "InvalidDataType",
            "set_technical_units invalid argument check failed.",
        )
        self.assertEqual(
            channel_api.set_technical_units(
                self.con_handle, "A", 1, 10, 10, 20.0
            ),
            "InvalidDataType",
            "set_technical_units invalid argument check failed.",
        )
        self.assertEqual(
            channel_api.set_technical_units(
                self.con_handle, "A", 1, "KGS", 10.0, 20
            ),
            "InvalidDataType",
            "set_technical_units invalid argument check failed.",
        )

    def test_get_auto_range(self):
        """Test get_auto_range api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "AutoRangeEnabled": 1,
                    "AutoRangeTime": 10.0,
                }
                self.assertEqual(
                    channel_api.get_auto_range(self.con_handle, "A", 1),
                    ("OK", "Enable", 10.0),
                    "get_auto_range success response test failed.",
                )

    def test_get_auto_range_neg(self):
        """Test get_auto_range api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "AutoRangeEnabled": 1,
                    "AutoRangeTime": 10.0,
                }
                self.assertEqual(
                    channel_api.get_auto_range(self.con_handle, "A", 1),
                    ("NOK", None, None),
                    "get_auto_range failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_auto_range(self.con_handle, "A", 1),
                    ("NOK", None, None),
                    "get_auto_range failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_auto_range(self.con_handle, "A", 1),
                    ("OK", None, None),
                    "get_auto_range failure response test failed.",
                )

    def test_get_auto_range_null_args(self):
        """Test get_auto_range api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_auto_range(self.con_handle, None, None),
            ("NullPtrArgument", None, None),
            "get_auto_range null argument check failed.",
        )

    def test_set_auto_range(self):
        """Test set_auto_range api with success response"""

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
                    channel_api.set_auto_range(
                        self.con_handle, "A", 1, "Enable", 10.0
                    ),
                    "OK",
                    "set_auto_range success response test failed.",
                )

    def test_set_auto_range_null_args(self):
        """Test set_auto_range api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_auto_range(
                self.con_handle, None, None, None, None
            ),
            "NullPtrArgument",
            "set_auto_range null argument check failed.",
        )

    def test_set_auto_range_invalid_args(self):
        """Test set_auto_range api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_auto_range(self.con_handle, "A", 1, "On", 10.0),
            "InvalidDataType",
            "set_auto_range invalid argument check failed.",
        )
        self.assertEqual(
            channel_api.set_auto_range(self.con_handle, "A", 1, "Enable", 10),
            "InvalidDataType",
            "set_auto_range invalid argument check failed.",
        )

    def test_cmd_auto_range_now(self):
        """Test cmd_auto_range_now api with success response"""

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
                    channel_api.cmd_auto_range_now(
                        self.con_handle, "A", 1, 10.0
                    ),
                    "OK",
                    "cmd_auto_range_now success response test failed.",
                )

    def test_cmd_auto_range_now_null_args(self):
        """Test cmd_auto_range_now api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.cmd_auto_range_now(self.con_handle, None, None, None),
            "NullPtrArgument",
            "cmd_auto_range_now null argument check failed.",
        )

    def test_cmd_auto_range_now_invalid_args(self):
        """Test cmd_auto_range_now api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.cmd_auto_range_now(self.con_handle, "A", 1, 10),
            "InvalidDataType",
            "cmd_auto_range_now invalid argument check failed.",
        )

    def test_get_channel_cal_info(self):
        """Test get_channel_cal_info api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "CalibrationDateTime": "01-01-2000",
                    "VerificationDateTime": "01-01-2000",
                    "PowerVerificationDateTime": "01-01-2000",
                    "CalibrationLab": "simCalLab2000",
                    "VerificationLab": "simCalLab2000",
                    "PowerVerificationLab": "simCalLab2000",
                }
                self.assertEqual(
                    channel_api.get_channel_cal_info(self.con_handle, "A", 1),
                    (
                        "OK",
                        "01-01-2000",
                        "01-01-2000",
                        "01-01-2000",
                        "simCalLab2000",
                        "simCalLab2000",
                        "simCalLab2000",
                    ),
                    "get_channel_cal_info success response test failed.",
                )

    def test_get_channel_cal_info_neg(self):
        """Test get_channel_cal_info api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "CalibrationDateTime": "01-01-2000",
                    "VerificationDateTime": "01-01-2000",
                    "PowerVerificationDateTime": "01-01-2000",
                    "CalibrationLab": "simCalLab2000",
                    "VerificationLab": "simCalLab2000",
                    "PowerVerificationLab": "simCalLab2000",
                }
                self.assertEqual(
                    channel_api.get_channel_cal_info(self.con_handle, "A", 1),
                    ("NOK", None, None, None, None, None, None),
                    "get_channel_cal_info failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_channel_cal_info(self.con_handle, "A", 1),
                    ("NOK", None, None, None, None, None, None),
                    "get_channel_cal_info failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_channel_cal_info(self.con_handle, "A", 1),
                    ("OK", None, None, None, None, None, None),
                    "get_channel_cal_info failure response test failed.",
                )

    def test_get_channel_cal_info_null_args(self):
        """Test get_channel_cal_info api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_channel_cal_info(self.con_handle, None, None),
            ("NullPtrArgument", None, None, None, None, None, None),
            "get_channel_cal_info null argument check failed.",
        )

    # Timer/Counter Module

    def test_get_timer_counter_gate_time(self):
        """Test get_timer_counter_gate_time api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "GateTime": 23.0,
                }
                self.assertEqual(
                    channel_api.get_timer_counter_gate_time(
                        self.con_handle, "A", 11
                    ),
                    ("OK", 23.0),
                    "get_timer_counter_gate_time success response test failed.",
                )

    def test_get_timer_counter_gate_time_neg(self):
        """Test get_timer_counter_gate_time api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "GateTime": 23.0,
                }
                self.assertEqual(
                    channel_api.get_timer_counter_gate_time(
                        self.con_handle, "A", 11
                    ),
                    ("NOK", None),
                    "get_timer_counter_gate_time failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_timer_counter_gate_time(
                        self.con_handle, "A", 11
                    ),
                    ("NOK", None),
                    "get_timer_counter_gate_time failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_timer_counter_gate_time(
                        self.con_handle, "A", 11
                    ),
                    ("OK", None),
                    "get_timer_counter_gate_time failure response test failed.",
                )

    def test_get_timer_counter_gate_time_null_args(self):
        """Test get_timer_counter_gate_time api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_timer_counter_gate_time(
                self.con_handle, None, None
            ),
            ("NullPtrArgument", None),
            "get_timer_counter_gate_time null argument check failed.",
        )

    def test_set_timer_counter_gate_time(self):
        """Test set_timer_counter_gate_time api with success response"""

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
                    channel_api.set_timer_counter_gate_time(
                        self.con_handle, "A", 11, 23.0
                    ),
                    "OK",
                    "set_timer_counter_gate_time success response test failed.",
                )

    def test_set_timer_counter_gate_time_null_args(self):
        """Test set_timer_counter_gate_time api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_timer_counter_gate_time(
                self.con_handle, None, None, None
            ),
            "NullPtrArgument",
            "set_timer_counter_gate_time null argument check failed.",
        )

    def test_set_timer_counter_gate_time_invalid_args(self):
        """Test set_timer_counter_gate_time api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_timer_counter_gate_time(
                self.con_handle, "A", 11, 20
            ),
            "InvalidDataType",
            "set_timer_counter_gate_time invalid argument check failed.",
        )

    def test_get_timer_counter_mode(self):
        """Test get_timer_counter_mode api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "TimerCounterMode": 8,
                }
                self.assertEqual(
                    channel_api.get_timer_counter_mode(
                        self.con_handle, "A", 11
                    ),
                    ("OK", "CountQuadrature"),
                    "get_timer_counter_mode success response test failed.",
                )

    def test_get_timer_counter_mode_neg(self):
        """Test get_timer_counter_mode api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "TimerCounterMode": 8,
                }
                self.assertEqual(
                    channel_api.get_timer_counter_mode(
                        self.con_handle, "A", 11
                    ),
                    ("NOK", None),
                    "get_timer_counter_mode failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_timer_counter_mode(
                        self.con_handle, "A", 11
                    ),
                    ("NOK", None),
                    "get_timer_counter_mode failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_timer_counter_mode(
                        self.con_handle, "A", 11
                    ),
                    ("OK", None),
                    "get_timer_counter_mode failure response test failed.",
                )

    def test_get_timer_counter_mode_null_args(self):
        """Test get_timer_counter_mode api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_timer_counter_mode(self.con_handle, None, None),
            ("NullPtrArgument", None),
            "get_timer_counter_mode null argument check failed.",
        )

    def test_set_timer_counter_mode(self):
        """Test set_timer_counter_mode api with success response"""

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
                    channel_api.set_timer_counter_mode(
                        self.con_handle, "A", 11, "CountQuadrature"
                    ),
                    "OK",
                    "set_timer_counter_mode success response test failed.",
                )

    def test_set_timer_counter_mode_null_args(self):
        """Test set_timer_counter_mode api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_timer_counter_mode(
                self.con_handle, None, None, None
            ),
            "NullPtrArgument",
            "set_timer_counter_mode null argument check failed.",
        )

    def test_set_timer_counter_mode_invalid_args(self):
        """Test set_timer_counter_mode api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_timer_counter_mode(
                self.con_handle, "A", 11, "Base"
            ),
            "InvalidDataType",
            "set_timer_counter_mode invalid argument check failed.",
        )

    def test_get_timer_counter_range(self):
        """Test get_timer_counter_range api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "LowerValue": 10.0,
                    "UpperValue": 20.0,
                }
                self.assertEqual(
                    channel_api.get_timer_counter_range(
                        self.con_handle, "A", 11
                    ),
                    ("OK", 10.0, 20.0),
                    "get_timer_counter_range success response test failed.",
                )

    def test_get_timer_counter_range_neg(self):
        """Test get_timer_counter_range api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "LowerValue": 10.0,
                    "UpperValue": 20.0,
                }
                self.assertEqual(
                    channel_api.get_timer_counter_range(
                        self.con_handle, "A", 11
                    ),
                    ("NOK", None, None),
                    "get_timer_counter_range failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    channel_api.get_timer_counter_range(
                        self.con_handle, "A", 11
                    ),
                    ("NOK", None, None),
                    "get_timer_counter_range failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    channel_api.get_timer_counter_range(
                        self.con_handle, "A", 11
                    ),
                    ("OK", None, None),
                    "get_timer_counter_range failure response test failed.",
                )

    def test_get_timer_counter_range_null_args(self):
        """Test get_timer_counter_range api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.get_timer_counter_range(self.con_handle, None, None),
            ("NullPtrArgument", None, None),
            "get_timer_counter_range null argument check failed.",
        )

    def test_set_timer_counter_range(self):
        """Test set_timer_counter_range api with success response"""

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
                    channel_api.set_timer_counter_range(
                        self.con_handle, "A", 11, 10.0, 20.0
                    ),
                    "OK",
                    "set_timer_counter_range success response test failed.",
                )

    def test_set_timer_counter_range_null_args(self):
        """Test set_timer_counter_range api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_timer_counter_range(
                self.con_handle, None, None, None, None
            ),
            "NullPtrArgument",
            "set_timer_counter_range null argument check failed.",
        )

    def test_set_timer_counter_range_invalid_args(self):
        """Test set_timer_counter_range api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            channel_api.set_timer_counter_range(
                self.con_handle, "A", 11, 10, 20.0
            ),
            "InvalidDataType",
            "set_timer_counter_range invalid argument check failed.",
        )
        self.assertEqual(
            channel_api.set_timer_counter_range(
                self.con_handle, "A", 11, 10.0, 20
            ),
            "InvalidDataType",
            "set_timer_counter_range invalid argument check failed.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Channel API Unittest Report",
            report_title="Channel API Unittest Report",
        )
    )
