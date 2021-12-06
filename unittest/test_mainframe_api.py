"""Mainframe API unit test."""

import os
import sys
import unittest
from unittest.mock import patch

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(os.path.join(parentdir, "src"))

from ghsapi import connection, ghsapi_states, mainframe_api


class TestMainframeAPI(unittest.TestCase):
    """Mainframe API unit test."""

    con_handle = connection.ConnectionHandler()
    GHSReturnValue = ghsapi_states.GHSReturnValue
    RETURN_KEY = ghsapi_states.RETURN_KEY

    def setUp(self):
        # run at start of test file
        pass

    def test_get_mainframe_info(self):
        """Test get_mainframe_info api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "MainframeType": "GenSimulator",
                    "MainframeName": "sim_DESKTOP-AH6RA3J",
                    "SerialNumber": "IDH312345",
                    "FirmwareVersion": "8.14.21160",
                }
                self.assertEqual(
                    mainframe_api.get_mainframe_info(self.con_handle),
                    (
                        "OK",
                        "GenSimulator",
                        "sim_DESKTOP-AH6RA3J",
                        "IDH312345",
                        "8.14.21160",
                    ),
                    "get_mainframe_info success response test failed.",
                )

    def test_get_mainframe_info_neg(self):
        """Test get_mainframe_info api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "MainframeType": "GenSimulator",
                    "MainframeName": "sim_DESKTOP-AH6RA3J",
                    "SerialNumber": "IDH312345",
                    "FirmwareVersion": "8.14.21160",
                }
                self.assertEqual(
                    mainframe_api.get_mainframe_info(self.con_handle),
                    ("NOK", None, None, None, None),
                    "get_mainframe_info failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    mainframe_api.get_mainframe_info(self.con_handle),
                    ("NOK", None, None, None, None),
                    "get_mainframe_info failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    mainframe_api.get_mainframe_info(self.con_handle),
                    ("OK", None, None, None, None),
                    "get_mainframe_info failure response test failed.",
                )

    def test_get_disk_space(self):
        """Test get_disk_space api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "TotalSize": 2.0,
                    "AvailableSize": 1.0,
                }
                self.assertEqual(
                    mainframe_api.get_disk_space(self.con_handle),
                    (
                        "OK",
                        2.0,
                        1.0,
                    ),
                    "get_disk_space success response test failed.",
                )

    def test_get_disk_space_neg(self):
        """Test get_disk_space api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "TotalSize": 2.0,
                    "AvailableSize": 1.0,
                }
                self.assertEqual(
                    mainframe_api.get_disk_space(self.con_handle),
                    ("NOK", None, None),
                    "get_disk_space failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    mainframe_api.get_disk_space(self.con_handle),
                    ("NOK", None, None),
                    "get_disk_space failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    mainframe_api.get_disk_space(self.con_handle),
                    ("OK", None, None),
                    "get_disk_space failure response test failed.",
                )

    def test_get_slot_count(self):
        """Test get_slot_count api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "SlotCount": 16,
                }
                self.assertEqual(
                    mainframe_api.get_slot_count(self.con_handle),
                    (
                        "OK",
                        16,
                    ),
                    "get_slot_count success response test failed.",
                )

    def test_get_slot_count_neg(self):
        """Test get_slot_count api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "SlotCount": 16,
                }
                self.assertEqual(
                    mainframe_api.get_slot_count(self.con_handle),
                    ("NOK", None),
                    "get_slot_count failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    mainframe_api.get_slot_count(self.con_handle),
                    ("NOK", None),
                    "get_slot_count failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    mainframe_api.get_slot_count(self.con_handle),
                    ("OK", None),
                    "get_slot_count failure response test failed.",
                )

    def test_get_sync_status(self):
        """Test get_sync_status api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "SyncStatus": 3,
                }
                self.assertEqual(
                    mainframe_api.get_sync_status(self.con_handle),
                    ("OK", "Synced"),
                    "get_sync_status success response test failed.",
                )

    def test_get_sync_status_neg(self):
        """Test get_sync_status api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "SyncStatus": "Synced",
                }
                self.assertEqual(
                    mainframe_api.get_sync_status(self.con_handle),
                    ("NOK", None),
                    "get_sync_status failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    mainframe_api.get_sync_status(self.con_handle),
                    ("NOK", None),
                    "get_sync_status failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    mainframe_api.get_sync_status(self.con_handle),
                    ("OK", None),
                    "get_sync_status failure response test failed.",
                )

    def test_get_user_mode(self):
        """Test get_user_mode api with success response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                    "UserMode": 2,
                }
                self.assertEqual(
                    mainframe_api.get_user_mode(self.con_handle),
                    ("OK", "Continuous"),
                    "get_user_mode success response test failed.",
                )

    def test_get_user_mode_neg(self):
        """Test get_user_mode api with failure response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:

            mock_con_est.return_value = self.GHSReturnValue["OK"]
            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                    "UserMode": 2,
                }
                self.assertEqual(
                    mainframe_api.get_user_mode(self.con_handle),
                    ("NOK", None),
                    "get_user_mode failure response test failed.",
                )
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"],
                }
                self.assertEqual(
                    mainframe_api.get_user_mode(self.con_handle),
                    ("NOK", None),
                    "get_user_mode failure response test failed.",
                )

                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["OK"],
                }
                self.assertEqual(
                    mainframe_api.get_user_mode(self.con_handle),
                    ("OK", None),
                    "get_user_mode failure response test failed.",
                )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Mainframe API Unittest Report",
            report_title="Mainframe API Unittest Report",
        )
    )
