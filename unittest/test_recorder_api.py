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

"""Recorder API unit test."""

import os
import sys
import unittest
from unittest.mock import patch

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(os.path.join(parentdir, "src"))

from ghsapi import connection, ghsapi_states, recorder_api


class TestRecorderAPI(unittest.TestCase):
    """Recorder API unit test."""

    con_handle = connection.ConnectionHandler()
    GHSReturnValue = ghsapi_states.GHSReturnValue
    RETURN_KEY = ghsapi_states.RETURN_KEY

    def setUp(self):
        # run at start of test file
        pass

    def test_get_channel_count(self):
        """Test get_channel_count api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "ChannelCount": 4,
                }
                self.assertEqual(
                    recorder_api.get_channel_count(self.con_handle, "A"),
                    (
                        "OK",
                        4,
                    ),
                    "get_channel_count success response test failed.",
                )

    def test_get_channel_count_neg(self):
        """Test get_channel_count api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "ChannelCount": 4,
                }
                self.assertEqual(
                    recorder_api.get_channel_count(self.con_handle, "A"),
                    ("NOK", None),
                    "get_channel_count failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    recorder_api.get_channel_count(self.con_handle, "A"),
                    ("NOK", None),
                    "get_channel_count failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    recorder_api.get_channel_count(self.con_handle, "A"),
                    ("OK", None),
                    "get_channel_count failure response test failed.",
                )

    def test_get_channel_count_null_args(self):
        """Test get_channel_count api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            recorder_api.get_channel_count(self.con_handle, None),
            ("NullPtrArgument", None),
            "get_channel_count null argument check failed.",
        )

    def test_get_digital_output(self):
        """Test get_digital_output api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "DigitalOutMode": 1,
                }
                self.assertEqual(
                    recorder_api.get_digital_output(
                        self.con_handle, "A", "Output1"
                    ),
                    (
                        "OK",
                        "High",
                    ),
                    "get_digital_output success response test failed.",
                )

    def test_get_digital_output_neg(self):
        """Test get_digital_output api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "DigitalOutMode": 1,
                }
                self.assertEqual(
                    recorder_api.get_digital_output(
                        self.con_handle, "A", "Output1"
                    ),
                    ("NOK", None),
                    "get_digital_output failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    recorder_api.get_digital_output(
                        self.con_handle, "A", "Output1"
                    ),
                    ("NOK", None),
                    "get_digital_output failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    recorder_api.get_digital_output(
                        self.con_handle, "A", "Output1"
                    ),
                    ("OK", None),
                    "get_digital_output failure response test failed.",
                )

    def test_get_digital_output_null_args(self):
        """Test get_digital_output api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            recorder_api.get_digital_output(self.con_handle, None, None),
            ("NullPtrArgument", None),
            "get_digital_output null argument check failed.",
        )

    def test_get_digital_output_invalid_args(self):
        """Test get_digital_output api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            recorder_api.get_digital_output(self.con_handle, "A", 3),
            ("InvalidOutputNumber", None),
            "get_digital_output invalid argument check failed.",
        )

    def test_get_recorder_enabled(self):
        """Test get_recorder_enabled api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "IsRecorderEnabled": 1,
                }
                self.assertEqual(
                    recorder_api.get_recorder_enabled(self.con_handle, "A"),
                    (
                        "OK",
                        "Enable",
                    ),
                    "get_recorder_enabled success response test failed.",
                )

    def test_get_recorder_enabled_neg(self):
        """Test get_recorder_enabled api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "IsRecorderEnabled": 1,
                }
                self.assertEqual(
                    recorder_api.get_recorder_enabled(self.con_handle, "A"),
                    ("NOK", None),
                    "get_recorder_enabled failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    recorder_api.get_recorder_enabled(self.con_handle, "A"),
                    ("NOK", None),
                    "get_recorder_enabled failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    recorder_api.get_recorder_enabled(self.con_handle, "A"),
                    ("OK", None),
                    "get_recorder_enabled failure response test failed.",
                )

    def test_get_recorder_enabled_null_args(self):
        """Test get_recorder_enabled api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            recorder_api.get_recorder_enabled(self.con_handle, None),
            ("NullPtrArgument", None),
            "get_recorder_enabled null argument check failed.",
        )

    def test_get_recorder_info(self):
        """Test get_recorder_info api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "RecorderType": "GenSimulator",
                    "RecorderName": "Recorder A",
                    "SerialNumber": "SIM0123456",
                    "FirmwareVersion": "8.22.21327",
                }
                self.assertEqual(
                    recorder_api.get_recorder_info(self.con_handle, "A"),
                    (
                        "OK",
                        "GenSimulator",
                        "Recorder A",
                        "SIM0123456",
                        "8.22.21327",
                    ),
                    "get_recorder_info success response test failed.",
                )

    def test_get_recorder_info_neg(self):
        """Test get_recorder_info api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "RecorderType": "GenSimulator",
                    "RecorderName": "Recorder A",
                    "SerialNumber": "SIM0123456",
                    "FirmwareVersion": "8.22.21327",
                }
                self.assertEqual(
                    recorder_api.get_recorder_info(self.con_handle, "A"),
                    ("NOK", None, None, None, None),
                    "get_recorder_info failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    recorder_api.get_recorder_info(self.con_handle, "A"),
                    ("NOK", None, None, None, None),
                    "get_recorder_info failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    recorder_api.get_recorder_info(self.con_handle, "A"),
                    ("OK", None, None, None, None),
                    "get_recorder_info failure response test failed.",
                )

    def test_get_recorder_info_null_args(self):
        """Test get_recorder_info api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            recorder_api.get_recorder_info(self.con_handle, None),
            ("NullPtrArgument", None, None, None, None),
            "get_recorder_info null argument check failed.",
        )

    def test_get_sample_rate(self):
        """Test get_sample_rate api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "SampleRate": 1000.0,
                }
                self.assertEqual(
                    recorder_api.get_sample_rate(self.con_handle, "A"),
                    (
                        "OK",
                        1000.0,
                    ),
                    "get_sample_rate success response test failed.",
                )

    def test_get_sample_rate_neg(self):
        """Test get_sample_rate api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "SampleRate": 1000.0,
                }
                self.assertEqual(
                    recorder_api.get_sample_rate(self.con_handle, "A"),
                    ("NOK", None),
                    "get_sample_rate failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    recorder_api.get_sample_rate(self.con_handle, "A"),
                    ("NOK", None),
                    "get_sample_rate failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    recorder_api.get_sample_rate(self.con_handle, "A"),
                    ("OK", None),
                    "get_sample_rate failure response test failed.",
                )

    def test_get_sample_rate_null_args(self):
        """Test get_sample_rate api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            recorder_api.get_sample_rate(self.con_handle, None),
            ("NullPtrArgument", None),
            "get_sample_rate null argument check failed.",
        )

    def test_set_digital_output(self):
        """Test set_digital_output api with success response"""

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
                    recorder_api.set_digital_output(
                        self.con_handle, "A", "Output1", "High"
                    ),
                    "OK",
                    "set_digital_output success response test failed.",
                )

    def test_set_digital_output_null_args(self):
        """Test set_digital_output api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            recorder_api.set_digital_output(self.con_handle, None, None, None),
            "NullPtrArgument",
            "set_digital_output null argument check failed.",
        )

    def test_set_digital_output_invalid_args(self):
        """Test set_digital_output api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            recorder_api.set_digital_output(
                self.con_handle, "A", "Output11", "High"
            ),
            "InvalidOutputNumber",
            "set_digital_output invalid argument check failed.",
        )

        self.assertEqual(
            recorder_api.set_digital_output(
                self.con_handle, "A", "Output1", "Up"
            ),
            "IncompatibleDigitalOutputMode",
            "set_digital_output invalid argument check failed.",
        )

    def test_set_recorder_enabled(self):
        """Test set_recorder_enabled api with success response"""

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
                    recorder_api.set_recorder_enabled(
                        self.con_handle, "A", "Enable"
                    ),
                    "OK",
                    "set_recorder_enabled success response test failed.",
                )

    def test_set_recorder_enabled_null_args(self):
        """Test set_recorder_enabled api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            recorder_api.set_recorder_enabled(self.con_handle, None, None),
            "NullPtrArgument",
            "set_recorder_enabled null argument check failed.",
        )

    def test_set_recorder_enabled_invalid_args(self):
        """Test set_recorder_enabled api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            recorder_api.set_recorder_enabled(self.con_handle, "A", "On"),
            "InvalidDataType",
            "set_recorder_enabled invalid argument check failed.",
        )

    def test_set_sample_rate(self):
        """Test set_sample_rate api with success response"""

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
                    recorder_api.set_sample_rate(self.con_handle, "A", 1000.0),
                    "OK",
                    "set_sample_rate success response test failed.",
                )

    def test_set_sample_rate_null_args(self):
        """Test set_sample_rate api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            recorder_api.set_sample_rate(self.con_handle, None, None),
            "NullPtrArgument",
            "set_sample_rate null argument check failed.",
        )

    def test_set_sample_rate_invalid_args(self):
        """Test set_sample_rate api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            recorder_api.set_sample_rate(self.con_handle, "A", "1000.0"),
            "InvalidDataType",
            "set_sample_rate invalid argument check failed.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Recorder API Unittest Report",
            report_title="Recorder API Unittest Report",
        )
    )
