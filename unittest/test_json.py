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

"""JSON create parse unit test."""

import json
import os
import sys
import unittest
from collections import OrderedDict

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(os.path.join(parentdir, "src"))

from ghsapi import ghsapi_states, json_rpc


class TestJSON(unittest.TestCase):
    """JSON create parse unit test."""

    GHSReturnValue = ghsapi_states.GHSReturnValue
    RETURN_KEY = ghsapi_states.RETURN_KEY

    def setUp(self):
        # run at start of test file
        self.request_id = 0

    def test_json_create(self):
        """Test JSON create request"""

        self.request_id += 1
        method_name = "Connect"
        method_param = {"ClientAPIVersion": 5}
        expected_json = OrderedDict(
            [
                ("jsonrpc", "2.0"),
                ("method", method_name),
                ("params", method_param),
                ("id", self.request_id),
            ]
        )
        expected_json = json.dumps(expected_json, separators=(",", ":")) + "\0"
        expected_json = expected_json.encode("utf-8")

        self.assertEqual(
            json_rpc.json_rpc_create_request(
                self.request_id, method_name, method_param
            ),
            expected_json,
            "JSON create request for connect failed.",
        )

        method_name = "Disconnect"
        method_param = 0
        expected_json = OrderedDict(
            [
                ("jsonrpc", "2.0"),
                ("method", method_name),
                ("id", self.request_id),
            ]
        )
        expected_json = json.dumps(expected_json, separators=(",", ":")) + "\0"
        expected_json = expected_json.encode("utf-8")

        self.assertEqual(
            json_rpc.json_rpc_create_request(
                self.request_id, method_name, method_param
            ),
            expected_json,
            "JSON create request for disconnect failed.",
        )

    def test_json_parse(self):
        """Test JSON parse response"""

        self.request_id = 1

        response_json = b'{"jsonrpc":"2.0","result":1,"id":2}\x00'
        self.assertEqual(
            json_rpc.json_rpc_parse_response(self.request_id, response_json)[
                self.RETURN_KEY
            ],
            self.GHSReturnValue["NOK"],
            "JSON parse reponse with invalid request id failed.",
        )

        response_json = b'{"jsonrpc": "2.0", "error": {"code": -32601, \
            "message": "Method not found"}, "id": 1}\x00'
        self.assertEqual(
            json_rpc.json_rpc_parse_response(self.request_id, response_json)[
                self.RETURN_KEY
            ],
            self.GHSReturnValue["MethodNotFound"],
            "JSON parse reponse with error code failed.",
        )

        response_json = b'{"jsonrpc": "2.0", "result": 7, "id": 1}\x00'
        self.assertEqual(
            json_rpc.json_rpc_parse_response(self.request_id, response_json)[
                self.RETURN_KEY
            ],
            self.GHSReturnValue["SystemNotRecording"],
            "JSON parse reponse with result as interger code failed.",
        )

        response_json = b'{"jsonrpc": "2.0", "result": {"GHSReturnValue": 18, \
            "message": "These are not the slots you are looking for"}, \
                "id": 1}\x00'
        self.assertEqual(
            json_rpc.json_rpc_parse_response(self.request_id, response_json)[
                self.RETURN_KEY
            ],
            self.GHSReturnValue["IncompatibleStorage"],
            "JSON parse with result in GHSReturnValue named parameter failed.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="JSON Unittest Report",
            report_title="JSON Unittest Report",
        )
    )
