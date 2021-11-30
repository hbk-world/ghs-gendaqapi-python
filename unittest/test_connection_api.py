"""Connection API unit test."""

import os
import sys
import unittest
from unittest.mock import patch

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(os.path.join(parentdir, "src"))

from ghsapi import connection, connection_api, ghsapi_states

IP_ADDRESS = "localhost"
PORT_NO = 8006
CLIENT_API_VERSION = 4


class TestConnectionAPI(unittest.TestCase):
    """Connection API unit test."""

    con_handle = connection.ConnectionHandler()
    GHSReturnValue = ghsapi_states.GHSReturnValue
    RETURN_KEY = ghsapi_states.RETURN_KEY

    def setUp(self):
        # run at start of test file
        pass

    def test_con_fail_to_est(self):
        """Test connect api with failed connection establish"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["NOK"]
            self.assertEqual(
                connection_api.connect(
                    self.con_handle, IP_ADDRESS, PORT_NO, CLIENT_API_VERSION
                ),
                "NOK",
                "Connect with not ok return check failed.",
            )

    def test_con_fail_to_send(self):
        """Test connect api with failed send request get response"""

        with patch(
            "test_connection_handler.connection.ConnectionHandler.connection_establish"
        ) as mock_con_est:
            mock_con_est.return_value = self.GHSReturnValue["OK"]

            with patch(
                "test_connection_handler.connection.ConnectionHandler.send_request_wait_response"
            ) as mock_req_ros:
                mock_req_ros.return_value = {
                    self.RETURN_KEY: self.GHSReturnValue["NOK"]
                }
                self.assertEqual(
                    connection_api.connect(
                        self.con_handle,
                        IP_ADDRESS,
                        PORT_NO,
                        CLIENT_API_VERSION,
                    ),
                    "NOK",
                    "Connect with not ok return check failed.",
                )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Connection API Unittest Report",
            report_title="Connection API Unittest Report",
        )
    )
