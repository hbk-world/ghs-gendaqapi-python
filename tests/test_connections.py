"""Docstring"""
import os
import sys
import unittest

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)
# sys.tracebacklimit = 0

from src import ghsapi


class TestConnections(unittest.TestCase):

    Gen7i = ghsapi.GHS()

    def test_connect(self):
        returnVar = self.Gen7i.GHSConnect("localhost", 8006)
        self.assertEqual(
            returnVar, "OK", "Failed to establishes a connection to the mainframe."
        )

    def test_get_client_api(self):
        returnVar = self.Gen7i.GHSGetClientAPIVersion()
        self.assertEqual(
            returnVar, 4, "Failed to get API version number of the client."
        )

    def test_disconnect(self):
        returnVar = self.Gen7i.GHSDisconnect()
        self.assertEqual(
            returnVar,
            "OK",
            "Failed to Disconnects from a connected mainframe.",
        )


if __name__ == "__main__":
    # unittest.main()
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Connections Unittest Report",
            report_title="Connections Unittest Report",
        )
    )
