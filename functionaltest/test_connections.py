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

"""Connections API functional test."""

import os
import sys
import unittest

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src.ghsapi import ghsapi

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
