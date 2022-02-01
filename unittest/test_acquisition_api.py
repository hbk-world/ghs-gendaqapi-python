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

"""Acquisition Control API unit test."""

import os
import sys
import unittest
from unittest.mock import patch

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(os.path.join(parentdir, "src"))

from ghsapi import acquisition_api, connection, ghsapi_states

ACQ_TIME = 3000.23
ABS_TIME_Y = 2021
ABS_TIME_D = 326
ABS_TIME_S = 3000.23


class TestAcquisitionAPI(unittest.TestCase):
    """Acquisition Control API unit test."""

    con_handle = connection.ConnectionHandler()
    GHSReturnValue = ghsapi_states.GHSReturnValue
    GHSAcquisitionState = ghsapi_states.GHSAcquisitionState
    RETURN_KEY = ghsapi_states.RETURN_KEY

    def setUp(self):
        # run at start of test file
        pass

    def test_get_acquisition_time(self):
        """Test get_acquisition_time api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    "AcquisitionTime": ACQ_TIME,
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    acquisition_api.get_acquisition_time(self.con_handle),
                    ("OK", ACQ_TIME),
                    "get_acquisition_time success response test failed.",
                )

    def test_get_acquisition_time_neg(self):
        """Test get_acquisition_time api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    "AcquisitionTime": ACQ_TIME,
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    acquisition_api.get_acquisition_time(self.con_handle),
                    ("NOK", None),
                    "get_acquisition_time failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    acquisition_api.get_acquisition_time(self.con_handle),
                    ("NOK", None),
                    "get_acquisition_time failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    acquisition_api.get_acquisition_time(self.con_handle),
                    ("OK", None),
                    "get_acquisition_time failure response test failed.",
                )

    def test_get_acquisition_start_time(self):
        """Test get_acquisition_start_time api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    "AbsoluteTimeYear": ABS_TIME_Y,
                    "AbsoluteTimeDay": ABS_TIME_D,
                    "AbsoluteTimeSeconds": ABS_TIME_S,
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    acquisition_api.get_acquisition_start_time(
                        self.con_handle
                    ),
                    ("OK", ABS_TIME_Y, ABS_TIME_D, ABS_TIME_S),
                    "get_acquisition_start_time success response test failed.",
                )

    def test_get_acquisition_start_time_neg(self):
        """Test get_acquisition_start_time api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    "AbsoluteTimeYear": ABS_TIME_Y,
                    "AbsoluteTimeDay": ABS_TIME_D,
                    "AbsoluteTimeSeconds": ABS_TIME_S,
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    acquisition_api.get_acquisition_start_time(
                        self.con_handle
                    ),
                    ("NOK", None, None, None),
                    "get_acquisition_start_time failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    acquisition_api.get_acquisition_start_time(
                        self.con_handle
                    ),
                    ("NOK", None, None, None),
                    "get_acquisition_start_time failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    acquisition_api.get_acquisition_start_time(
                        self.con_handle
                    ),
                    ("OK", None, None, None),
                    "get_acquisition_start_time failure response test failed.",
                )

    def test_get_acquisition_state(self):
        """Test get_acquisition_state api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    "GHSAcquisitionState": self.GHSAcquisitionState[
                        "Recording"
                    ],
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    acquisition_api.get_acquisition_state(self.con_handle),
                    ("OK", "Recording"),
                    "get_acquisition_state success response test failed.",
                )

    def test_get_acquisition_state_neg(self):
        """Test get_acquisition_state api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    "GHSAcquisitionState": self.GHSAcquisitionState[
                        "Recording"
                    ],
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    acquisition_api.get_acquisition_state(self.con_handle),
                    ("NOK", None),
                    "get_acquisition_state success response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    acquisition_api.get_acquisition_state(self.con_handle),
                    ("NOK", None),
                    "get_acquisition_state success response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    acquisition_api.get_acquisition_state(self.con_handle),
                    ("OK", None),
                    "get_acquisition_state success response test failed.",
                )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Acquisition Control API Unittest Report",
            report_title="Acquisition Control API Unittest Report",
        )
    )
