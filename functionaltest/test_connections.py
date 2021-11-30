"""Connections API fucntional test."""

import os
import sys
import unittest

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src import ghsapi

IP_ADDRESS = "localhost"
PORT_NO = 8006
CLIENT_API_VERSION = 4


class TestConnections(unittest.TestCase):
    """Connections API functional test."""

    gen = ghsapi.GHS()

    def test_connect(self):
        """Test connect."""

        return_var = self.gen.ghs_connect(IP_ADDRESS, PORT_NO)
        self.assertEqual(
            return_var,
            "OK",
            "Failed to establishes a connection to the mainframe.",
        )

    def test_get_client_api(self):
        """Test get api."""

        return_var = self.gen.ghs_get_client_api_version()
        self.assertEqual(
            return_var,
            CLIENT_API_VERSION,
            "Client API version number mismatch.",
        )

    def test_disconnect(self):
        """Test disconnect."""

        return_var = self.gen.ghs_disconnect()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to Disconnects from a connected mainframe.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Connections API Functional Test Report",
            report_title="Connections API Functional Test Report",
        )
    )
