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

"""Manage recordings API unit test."""

import os
import sys
import unittest
from unittest.mock import patch

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(os.path.join(parentdir, "src"))

from ghsapi import connection, ghsapi_states, manage_recordings_api


class TestManageRecordingsAPI(unittest.TestCase):
    """Manage recordings API unit test."""

    con_handle = connection.ConnectionHandler()
    GHSReturnValue = ghsapi_states.GHSReturnValue
    RETURN_KEY = ghsapi_states.RETURN_KEY

    def setUp(self):
        # run at start of test file
        pass

    def test_get_recording_name(self):
        """Test get_recording_name api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "RecordingName": "Test1",
                    "RecordingIndex": 2,
                }
                self.assertEqual(
                    manage_recordings_api.get_recording_name(self.con_handle),
                    (
                        "OK",
                        "Test1",
                        2,
                    ),
                    "get_recording_name success response test failed.",
                )

    def test_get_recording_name_info_neg(self):
        """Test get_recording_name api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "RecordingName": "Test1",
                    "RecordingIndex": 2,
                }
                self.assertEqual(
                    manage_recordings_api.get_recording_name(self.con_handle),
                    ("NOK", None, None),
                    "get_recording_name failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    manage_recordings_api.get_recording_name(self.con_handle),
                    ("NOK", None, None),
                    "get_recording_name failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    manage_recordings_api.get_recording_name(self.con_handle),
                    ("OK", None, None),
                    "get_recording_name failure response test failed.",
                )

    def test_set_recording_name_null_args(self):
        """Test set_recording_name api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            manage_recordings_api.set_recording_name(
                self.con_handle, None, None
            ),
            "NullPtrArgument",
            "set_recording_name null argument check failed.",
        )

    def test_get_storage_location(self):
        """Test get_storage_location api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "StorageLocation": 2,
                }
                self.assertEqual(
                    manage_recordings_api.get_storage_location(
                        self.con_handle
                    ),
                    (
                        "OK",
                        "Local1",
                    ),
                    "get_storage_location success response test failed.",
                )

    def test_get_storage_location_info_neg(self):
        """Test get_storage_location api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "GetStorageLocation": "Local1",
                }
                self.assertEqual(
                    manage_recordings_api.get_storage_location(
                        self.con_handle
                    ),
                    ("NOK", None),
                    "get_storage_location failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    manage_recordings_api.get_storage_location(
                        self.con_handle
                    ),
                    ("NOK", None),
                    "get_storage_location failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    manage_recordings_api.get_storage_location(
                        self.con_handle
                    ),
                    ("OK", None),
                    "get_storage_location failure response test failed.",
                )

    def test_set_storage_location_null_args(self):
        """Test set_storage_location api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            manage_recordings_api.set_storage_location(self.con_handle, None),
            "NullPtrArgument",
            "set_storage_location null argument check failed.",
        )

    def test_set_storage_location_invalid_args(self):
        """Test set_storage_location api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            manage_recordings_api.set_storage_location(self.con_handle, 8),
            "IncompatibleStorage",
            "set_storage_location invalid argument check failed.",
        )

        self.assertEqual(
            manage_recordings_api.set_storage_location(
                self.con_handle, "Local404"
            ),
            "IncompatibleStorage",
            "set_storage_location invalid argument check failed.",
        )

    def test_get_high_low_rate_storage_enabled_null_args(self):
        """Test get_high_low_rate_storage_enabled api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            manage_recordings_api.get_high_low_rate_storage_enabled(
                self.con_handle, None, None
            ),
            "NullPtrArgument",
            "get_high_low_rate_storage_enabled null argument check failed.",
        )

    def test_get_high_low_rate_storage_enabled_invalid_args(self):
        """Test get_high_low_rate_storage_enabled api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            manage_recordings_api.get_high_low_rate_storage_enabled(
                self.con_handle, "Channels", "A"
            ),
            "InvalidDataType",
            "get_high_low_rate_storage_enabled invalid argument check failed.",
        )

        self.assertEqual(
            manage_recordings_api.get_high_low_rate_storage_enabled(
                self.con_handle, 404, "A"
            ),
            "InvalidDataType",
            "get_high_low_rate_storage_enabled invalid argument check failed.",
        )

    def test_set_high_low_rate_storage_enabled_null_args(self):
        """Test set_high_low_rate_storage_enabled api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            manage_recordings_api.set_high_low_rate_storage_enabled(
                self.con_handle, None, None, None, None
            ),
            "NullPtrArgument",
            "set_high_low_rate_storage_enabled null argument check failed.",
        )

    def test_set_high_low_rate_storage_enabled_invalid_args(self):
        """Test set_high_low_rate_storage_enabled api with invalid args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            manage_recordings_api.set_high_low_rate_storage_enabled(
                self.con_handle, "Channels", "A", "Enable", "Enable"
            ),
            "InvalidDataType",
            "set_high_low_rate_storage_enabled invalid argument check failed.",
        )

        self.assertEqual(
            manage_recordings_api.set_high_low_rate_storage_enabled(
                self.con_handle, "SyncChannels", "A", "able", "Enable"
            ),
            "InvalidDataType",
            "set_high_low_rate_storage_enabled invalid argument check failed.",
        )

        self.assertEqual(
            manage_recordings_api.set_high_low_rate_storage_enabled(
                self.con_handle, "SyncChannels", "A", "Enable", "able"
            ),
            "InvalidDataType",
            "set_high_low_rate_storage_enabled invalid argument check failed.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Manage recordings API Unittest Report",
            report_title="Manage recordings API Unittest Report",
        )
    )
