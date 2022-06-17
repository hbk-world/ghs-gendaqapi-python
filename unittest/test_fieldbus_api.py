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

"""FieldBus API unit test."""

import os
import sys
import unittest
from unittest.mock import patch

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(os.path.join(parentdir, "src"))

from ghsapi import connection, fieldbus_api, ghsapi_states


class TestFieldbusAPI(unittest.TestCase):
    """FieldBus API unit test."""

    con_handle = connection.ConnectionHandler()
    GHSReturnValue = ghsapi_states.GHSReturnValue
    RETURN_KEY = ghsapi_states.RETURN_KEY

    def setUp(self):
        # run at start of test file
        pass

    def test_initiate_fieldbus_data_transfer(self):
        """Test initiate_fieldbus_data_transfer api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "UpdateRate": 1,
                    "DataCount": 2,
                }
                self.assertEqual(
                    fieldbus_api.initiate_fieldbus_data_transfer(
                        self.con_handle, 1
                    ),
                    (
                        "OK",
                        1,
                        2,
                    ),
                    "initiate_fieldbus_data_transfer success response test failed.",
                )

    def test_initiate_fieldbus_data_transfer_neg(self):
        """Test initiate_fieldbus_data_transfer api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "UpdateRate": 1,
                    "DataCount": 2,
                }
                self.assertEqual(
                    fieldbus_api.initiate_fieldbus_data_transfer(
                        self.con_handle, 1
                    ),
                    ("NOK", None, None),
                    "initiate_fieldbus_data_transfer failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    fieldbus_api.initiate_fieldbus_data_transfer(
                        self.con_handle, 1
                    ),
                    ("NOK", None, None),
                    "initiate_fieldbus_data_transfer failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    fieldbus_api.initiate_fieldbus_data_transfer(
                        self.con_handle, 1
                    ),
                    ("OK", None, None),
                    "initiate_fieldbus_data_transfer failure response test failed.",
                )

    def test_initiate_fieldbus_data_transfer_null_args(self):
        """Test initiate_fieldbus_data_transfer api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            fieldbus_api.initiate_fieldbus_data_transfer(
                self.con_handle, None
            ),
            ("NullPtrArgument", None, None),
            "initiate_fieldbus_data_transfer null argument check failed.",
        )

    def test_stop_fieldbus_data_transfer(self):
        """Test stop_fieldbus_data_transfer api with success response"""

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
                    fieldbus_api.stop_fieldbus_data_transfer(self.con_handle),
                    "OK",
                    "stop_fieldbus_data_transfer success response test failed.",
                )

    def test_get_fieldbus_data_count(self):
        """Test get_fieldbus_data_count api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "DataCount": 2,
                }
                self.assertEqual(
                    fieldbus_api.get_fieldbus_data_count(self.con_handle),
                    (
                        "OK",
                        2,
                    ),
                    "get_fieldbus_data_count success response test failed.",
                )

    def test_get_fieldbus_data_count_neg(self):
        """Test get_fieldbus_data_count api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "DataCount": 2,
                }
                self.assertEqual(
                    fieldbus_api.get_fieldbus_data_count(self.con_handle),
                    ("NOK", None),
                    "get_fieldbus_data_count failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    fieldbus_api.get_fieldbus_data_count(self.con_handle),
                    ("NOK", None),
                    "get_fieldbus_data_count failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    fieldbus_api.get_fieldbus_data_count(self.con_handle),
                    ("OK", None),
                    "get_fieldbus_data_count failure response test failed.",
                )

    def test_get_fieldbus_data_name_and_unit(self):
        """Test get_fieldbus_data_name_and_unit api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "DataName": "Latency",
                    "DataUnit": "s",
                }
                self.assertEqual(
                    fieldbus_api.get_fieldbus_data_name_and_unit(
                        self.con_handle, 1
                    ),
                    (
                        "OK",
                        "Latency",
                        "s",
                    ),
                    "get_fieldbus_data_name_and_unit success response test failed.",
                )

    def test_get_fieldbus_data_name_and_unit_neg(self):
        """Test get_fieldbus_data_name_and_unit api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "DataName": "Latency",
                    "DataUnit": "s",
                }
                self.assertEqual(
                    fieldbus_api.get_fieldbus_data_name_and_unit(
                        self.con_handle, 1
                    ),
                    ("NOK", None, None),
                    "get_fieldbus_data_name_and_unit failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    fieldbus_api.get_fieldbus_data_name_and_unit(
                        self.con_handle, 1
                    ),
                    ("NOK", None, None),
                    "get_fieldbus_data_name_and_unit failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    fieldbus_api.get_fieldbus_data_name_and_unit(
                        self.con_handle, 1
                    ),
                    ("OK", None, None),
                    "get_fieldbus_data_name_and_unit failure response test failed.",
                )

    def test_get_fieldbus_data_name_and_unit_null_args(self):
        """Test get_fieldbus_data_name_and_unit api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            fieldbus_api.get_fieldbus_data_name_and_unit(
                self.con_handle, None
            ),
            ("NullPtrArgument", None, None),
            "get_fieldbus_data_name_and_unit null argument check failed.",
        )

    def test_request_fieldbus_snapshot_count(self):
        """Test request_fieldbus_snapshot api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "TimeStamp": 0.999465000000986,
                    "DataCount": 2,
                    "Data": [1.0, 0.0010000000474974513],
                }
                self.assertEqual(
                    fieldbus_api.request_fieldbus_snapshot(self.con_handle),
                    (
                        "OK",
                        0.999465000000986,
                        2,
                        [1.0, 0.0010000000474974513],
                    ),
                    "request_fieldbus_snapshot success response test failed.",
                )

    def test_request_fieldbus_snapshot_neg(self):
        """Test request_fieldbus_snapshot api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "TimeStamp": 0.999465000000986,
                    "DataCount": 2,
                    "Data": [1.0, 0.0010000000474974513],
                }
                self.assertEqual(
                    fieldbus_api.request_fieldbus_snapshot(self.con_handle),
                    ("NOK", None, None, None),
                    "request_fieldbus_snapshot failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    fieldbus_api.request_fieldbus_snapshot(self.con_handle),
                    ("NOK", None, None, None),
                    "request_fieldbus_snapshot failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    fieldbus_api.request_fieldbus_snapshot(self.con_handle),
                    ("OK", None, None, None),
                    "request_fieldbus_snapshot failure response test failed.",
                )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="FieldBus API Unittest Report",
            report_title="FieldBus API Unittest Report",
        )
    )
