"""Manage mainframe settings API unit test."""

import os
import sys
import unittest
from unittest.mock import patch

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(os.path.join(parentdir, "src"))

from ghsapi import connection, ghsapi_states, manage_mainframe_settings


class TestManageMainframeSettingsAPI(unittest.TestCase):
    """Manage mainframe settings API unit test."""

    con_handle = connection.ConnectionHandler()
    GHSReturnValue = ghsapi_states.GHSReturnValue
    RETURN_KEY = ghsapi_states.RETURN_KEY

    def setUp(self):
        # run at start of test file
        pass

    def test_get_current_settings(self):
        """Test get_current_settings api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "Size": 4,
                    "Blob": b"test",
                }
                self.assertEqual(
                    manage_mainframe_settings.get_current_settings(
                        self.con_handle
                    ),
                    (
                        "OK",
                        b"test",
                        4,
                    ),
                    "get_current_settings success response test failed.",
                )

    def test_get_current_settings_neg(self):
        """Test get_current_settings api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "Size": 4,
                    "Blob": b"test",
                }
                self.assertEqual(
                    manage_mainframe_settings.get_current_settings(
                        self.con_handle
                    ),
                    ("NOK", None, None),
                    "get_current_settings failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    manage_mainframe_settings.get_current_settings(
                        self.con_handle
                    ),
                    ("NOK", None, None),
                    "get_current_settings failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    manage_mainframe_settings.get_current_settings(
                        self.con_handle
                    ),
                    ("OK", None, None),
                    "get_current_settings failure response test failed.",
                )

    def test_set_current_settings_null_args(self):
        """Test set_current_settings api with null args"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

        self.assertEqual(
            manage_mainframe_settings.set_current_settings(
                self.con_handle, None, None
            ),
            "NullPtrArgument",
            "set_current_settings null argument check failed.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Manage mainframe settings API Unittest Report",
            report_title="Manage mainframe settings API Unittest Report",
        )
    )
