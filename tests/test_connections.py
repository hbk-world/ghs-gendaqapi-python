"""Connections API unit test."""

import os
import sys
import unittest

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src import ghsapi


class TestConnections(unittest.TestCase):
    """Connections API unit test."""

    gen = ghsapi.GHS()

    def test_connect(self):
        """Test connect."""

        return_var = self.gen.ghs_connect("localhost", 8006)
        self.assertEqual(
            return_var,
            "OK",
            "Failed to establishes a connection to the mainframe.",
        )

    def test_get_client_api(self):
        """Test get api."""

        return_var = self.gen.ghs_get_client_api_version()
        self.assertEqual(return_var, 4, "Client API version number mismatch.")

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
            report_name="Connections Unittest Report",
            report_title="Connections Unittest Report",
        )
    )
