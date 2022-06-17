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

"""FieldBus API functional test."""

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


class TestFieldbus(unittest.TestCase):
    """FieldBus API functional test."""

    gen = ghsapi.GHS()

    @classmethod
    def setUpClass(cls):
        # run connect api at start of test file
        cls.gen.ghs_connect(IP_ADDRESS, PORT_NO)

    @classmethod
    def tearDownClass(cls):
        # run disconnect api at end of test file
        cls.gen.ghs_disconnect()

    def setUp(self):
        # runs before each test
        pass

    def tearDown(self):
        # runs after each test
        self.gen.ghs_stop_fieldbus_data_transfer()
        self.gen.ghs_stop_preview()

    def test_initiate_fieldbus_data_transfer(self):
        """Test initiate fieldbus"""

        (
            return_var,
            update_rate,
            data_count,
        ) = self.gen.ghs_initiate_fieldbus_data_transfer(1)
        self.assertEqual(
            isinstance(update_rate, int),
            True,
            "Failed on get update rate.",
        )
        self.assertEqual(
            update_rate,
            1,
            "Failed to set update rate.",
        )
        self.assertEqual(
            isinstance(data_count, int),
            True,
            "Failed on get data count.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on initiate fieldbus.",
        )

    def test_double_initiate_fieldbus_data_transfer(self):
        """Test initiate fieldbus when already initiated"""

        self.gen.ghs_initiate_fieldbus_data_transfer(1)

        (
            return_var,
            update_rate,
            data_count,
        ) = self.gen.ghs_initiate_fieldbus_data_transfer(1)
        self.assertEqual(
            return_var,
            "FieldBusAlready_Enabled",
            "Failed on initiate fieldbus when already initiated",
        )

    def test_get_fieldbus_data_count(self):
        """Test to get fieldbus data count"""

        (
            return_var,
            data_count,
        ) = self.gen.ghs_get_fieldbus_data_count()
        self.assertEqual(
            isinstance(data_count, int),
            True,
            "Failed on get data count.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get data count.",
        )

    def test_get_fieldbus_data_name_and_unit(self):
        """Test to get fieldbus data name and unit"""

        (
            return_var,
            data_name,
            data_unit,
        ) = self.gen.ghs_get_fieldbus_data_name_and_unit(1)
        self.assertEqual(
            isinstance(data_name, str),
            True,
            "Failed on get data name.",
        )
        self.assertEqual(
            isinstance(data_unit, str),
            True,
            "Failed on get data unit.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get data name and unit.",
        )

    def test_get_invalid_fieldbus_data_name_and_unit(self):
        """Test to get invalid fieldbus data name and unit"""

        (
            return_var,
            data_name,
            data_unit,
        ) = self.gen.ghs_get_fieldbus_data_name_and_unit(20)
        self.assertEqual(
            return_var,
            "InvalidChannelIndex",
            "Failed on get invalid data name and unit.",
        )

    def test_request_fieldbus_snapshot(self):
        """Test to request fieldbus snapshot"""

        return_var = self.gen.ghs_start_preview()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on start preview.",
        )

        (
            return_var,
            time_stamp,
            data_count,
            data,
        ) = self.gen.ghs_request_fieldbus_snapshot()
        self.assertEqual(
            isinstance(time_stamp, float),
            True,
            "Failed on get time stamp.",
        )
        self.assertEqual(
            isinstance(data_count, int),
            True,
            "Failed on get data count.",
        )
        self.assertEqual(
            isinstance(data, list),
            True,
            "Failed on get data.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on request fieldbus snapshot.",
        )

    def test_request_fieldbus_snapshot_not_acquiring(self):
        """Test to request fieldbus snapshot when not acquiring"""
        (
            return_var,
            time_stamp,
            data_count,
            data,
        ) = self.gen.ghs_request_fieldbus_snapshot()
        self.assertEqual(
            return_var,
            "SystemNotRecording",
            "Failed on request fieldbus snapshot when not acquiring.",
        )

    def test_request_fieldbus_snapshot_when_enabled(self):
        """Test to request fieldbus snapshot when fieldbus is enabled"""

        (
            return_var,
            update_rate,
            data_count,
        ) = self.gen.ghs_initiate_fieldbus_data_transfer(1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on initiate fieldbus.",
        )

        return_var = self.gen.ghs_start_preview()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on start preview.",
        )

        (
            return_var,
            time_stamp,
            data_count,
            data,
        ) = self.gen.ghs_request_fieldbus_snapshot()
        self.assertEqual(
            return_var,
            "FieldBusAlready_Enabled",
            "Failed on request fieldbus snapshot when fieldbus is enabled.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="FieldBus API Functional Test Report",
            report_title="FieldBus API Functional Test Report",
        )
    )
