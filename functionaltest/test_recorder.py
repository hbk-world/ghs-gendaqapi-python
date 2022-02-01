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

"""Recorder API functional test."""

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


class TestRecorder(unittest.TestCase):
    """Recorder API functional test."""

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
        pass

    def test_get_channel_count(self):
        """Test get channel count return type to be integer"""

        return_var, channel_count = self.gen.ghs_get_channel_count("A")
        self.assertEqual(
            isinstance(channel_count, int),
            True,
            "Failed on get channel count.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get channel count.",
        )

    def test_channel_count_recorder_disable(self):
        """Test get channel count when recorder disabled"""

        return_var, channel_count = self.gen.ghs_get_channel_count("A")
        self.assertEqual(
            isinstance(channel_count, int),
            True,
            "Failed on get channel count.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get channel count.",
        )

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var, channel_count_2 = self.gen.ghs_get_channel_count("A")
        self.assertEqual(
            isinstance(channel_count_2, int),
            True,
            "Failed on get channel count.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get channel count.",
        )
        self.assertEqual(
            channel_count == channel_count_2,
            True,
            "Failed to get correct channel count.",
        )

    def test_get_digital_output(self):
        """Test get digital output mode"""

        return_var, output_mode = self.gen.ghs_get_digital_output(
            "A", "Output1"
        )
        self.assertEqual(
            output_mode in ghsapi.GHSDigitalOutMode,
            True,
            "Failed on get digital output mode.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get digital output mode.",
        )

        return_var, output_mode = self.gen.ghs_get_digital_output(
            "A", "Output2"
        )
        self.assertEqual(
            output_mode in ghsapi.GHSDigitalOutMode,
            True,
            "Failed on get digital output mode.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get digital output mode.",
        )

    def test_set_digital_output1(self):
        """Test set digital output1"""

        return_var = self.gen.ghs_set_digital_output("A", "Output1", "Low")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set digital output mode.",
        )
        return_var, output_mode = self.gen.ghs_get_digital_output(
            "A", "Output1"
        )
        self.assertEqual(
            output_mode,
            "Low",
            "Failed on get correct digital output mode.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get correct digital output mode.",
        )

        return_var = self.gen.ghs_set_digital_output("A", "Output1", "High")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set digital output mode.",
        )
        return_var, output_mode = self.gen.ghs_get_digital_output(
            "A", "Output1"
        )
        self.assertEqual(
            output_mode,
            "High",
            "Failed on get correct digital output mode.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get correct digital output mode.",
        )

        return_var = self.gen.ghs_set_digital_output("A", "Output1", "Trigger")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set digital output mode.",
        )
        return_var, output_mode = self.gen.ghs_get_digital_output(
            "A", "Output1"
        )
        self.assertEqual(
            output_mode,
            "Trigger",
            "Failed on get correct digital output mode.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get correct digital output mode.",
        )

        return_var = self.gen.ghs_set_digital_output("A", "Output1", "Alarm")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set digital output mode.",
        )
        return_var, output_mode = self.gen.ghs_get_digital_output(
            "A", "Output1"
        )
        self.assertEqual(
            output_mode,
            "Alarm",
            "Failed on get correct digital output mode.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get correct digital output mode.",
        )

    def test_set_incorrect_digital_output1(self):
        """Test set incorrect digital output1"""

        return_var = self.gen.ghs_set_digital_output(
            "A", "Output1", "Acquiring"
        )
        self.assertEqual(
            return_var,
            "IncompatibleDigitalOutputMode",
            "Failed on set incorrect digital output mode.",
        )

    def test_set_digital_output2(self):
        """Test set digital output2"""

        return_var = self.gen.ghs_set_digital_output("A", "Output2", "Low")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set digital output mode.",
        )
        return_var, output_mode = self.gen.ghs_get_digital_output(
            "A", "Output2"
        )
        self.assertEqual(
            output_mode,
            "Low",
            "Failed on get correct digital output mode.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get correct digital output mode.",
        )

        return_var = self.gen.ghs_set_digital_output("A", "Output2", "High")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set digital output mode.",
        )
        return_var, output_mode = self.gen.ghs_get_digital_output(
            "A", "Output2"
        )
        self.assertEqual(
            output_mode,
            "High",
            "Failed on get correct digital output mode.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get correct digital output mode.",
        )

        return_var = self.gen.ghs_set_digital_output(
            "A", "Output2", "Acquiring"
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set digital output mode.",
        )
        return_var, output_mode = self.gen.ghs_get_digital_output(
            "A", "Output2"
        )
        self.assertEqual(
            output_mode,
            "Acquiring",
            "Failed on get correct digital output mode.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get correct digital output mode.",
        )

    def test_set_incorrect_digital_output2(self):
        """Test set incorrect digital output2"""

        return_var = self.gen.ghs_set_digital_output("A", "Output2", "Trigger")
        self.assertEqual(
            return_var,
            "IncompatibleDigitalOutputMode",
            "Failed on set incorrect digital output mode.",
        )

        return_var = self.gen.ghs_set_digital_output("A", "Output2", "Alarm")
        self.assertEqual(
            return_var,
            "IncompatibleDigitalOutputMode",
            "Failed on set incorrect digital output mode.",
        )

    def test_set_get_recorder_enabled(self):
        """Test set and get recorder enabled"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set recorder enabled.",
        )

        return_var, enabled = self.gen.ghs_get_recorder_enabled("A")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get recorder enabled.",
        )
        self.assertEqual(
            enabled,
            "Disable",
            "Failed on get recorder enabled.",
        )

    def test_get_recorder_info(self):
        """Test to get recorder information."""

        return_var = self.gen.ghs_get_recorder_info("A")
        result_type = (
            return_var[0] == "OK"
            and isinstance(return_var[1], str)
            and isinstance(return_var[2], str)
            and isinstance(return_var[3], str)
            and isinstance(return_var[4], str)
        )
        self.assertEqual(
            result_type,
            True,
            "Failed to get recorder information.",
        )

    def test_set_get_sample_rate(self):
        """Test set and get sample rate of recorder"""

        return_var = self.gen.ghs_set_sample_rate("A", 1000.0)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set recorder sample rate.",
        )

        return_var, sample_rate = self.gen.ghs_get_sample_rate("A")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get recorder sample rate.",
        )
        self.assertEqual(
            sample_rate,
            1000.0,
            "Failed on get recorder sample rate.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Recorder API Functional Test Report",
            report_title="Recorder API Functional Test Report",
        )
    )
