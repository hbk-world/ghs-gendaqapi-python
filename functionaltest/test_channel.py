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

"""Channel API functional test."""

import os
import sys
import time
import unittest

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src.ghsapi import ghsapi

IP_ADDRESS = "localhost"
PORT_NO = 8006


class TestChannel(unittest.TestCase):
    """Channel API functional test."""

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
        self.gen.ghs_stop_recording()
        self.gen.ghs_set_recorder_enabled("A", "Enable")

    def test_get_channel_type(self):
        """Test get channel type and it's return value"""

        return_var, channel_type = self.gen.ghs_get_channel_type("A", 1)
        self.assertEqual(
            channel_type in ghsapi.GHSChannelType,
            True,
            "Failed on get channel type.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get channel type.",
        )

    def test_get_channel_type_recorder_disabled(self):
        """Test get channel type when recorder is disabled"""

        return_var, channel_type = self.gen.ghs_get_channel_type("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get channel type.",
        )

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var, channel_type_dis = self.gen.ghs_get_channel_type("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get channel type.",
        )
        self.assertEqual(
            channel_type == channel_type_dis,
            True,
            "Failed on get channel type when recorder disabled.",
        )

    def test_get_invalid_channel_type(self):
        """Test get type of invalid channel"""

        return_var = self.gen.ghs_get_channel_type("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get type of invalid channel.",
        )

    def test_set_get_channel_name(self):
        """Test set and get channel name"""

        return_var = self.gen.ghs_set_channel_name("A", 1, "TestName")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set channel name.",
        )
        return_var, channel_name = self.gen.ghs_get_channel_name("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get channel name.",
        )
        self.assertEqual(
            channel_name,
            "TestName",
            "Failed to set correct channel name.",
        )

    def test_set_invalid_channel_name(self):
        """Test set invalid channel name"""

        return_var = self.gen.ghs_set_channel_name("A", 1, 123)
        self.assertEqual(
            return_var,
            "InvalidDataType",
            "Failed on set invalid channel name.",
        )

    def test_set_to_invalid_channel_name(self):
        """Test set name to invalid channel"""

        return_var = self.gen.ghs_set_channel_name("Z", 100, "TestName")
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set name to invalid channel.",
        )

    def test_set_channel_name_disabled_recorder(self):
        """Test set channel name of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_channel_name("A", 1, "TestName2")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set channel name of disabled recorder.",
        )
        return_var, channel_name = self.gen.ghs_get_channel_name("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get channel name of disabled recorder.",
        )
        self.assertEqual(
            channel_name,
            "TestName2",
            "Failed to set correct channel name of disabled recorder.",
        )

    def test_set_duplicate_channel_name(self):
        """Test set duplicate channel name on two channel"""

        return_var = self.gen.ghs_set_channel_name("A", 1, "TestName")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set name to channel 1.",
        )
        return_var = self.gen.ghs_set_channel_name("A", 2, "TestName")
        self.assertEqual(
            return_var,
            "DuplicateChannelName",
            "Failed on set duplicate name to channel 2.",
        )

    def test_get_invalid_channel_name(self):
        """Test get invalid channel's name"""

        return_var = self.gen.ghs_get_channel_name("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get name of invalid channel.",
        )

    def test_get_channel_name_disabled_recorder(self):
        """Test get channel name of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_channel_name("A", 1)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get channel name of disabled recorder.",
        )

    def test_get_channel_name_type(self):
        """Test get channel name type"""

        return_var, channel_name = self.gen.ghs_get_channel_name("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get channel name.",
        )
        self.assertEqual(
            isinstance(channel_name, str),
            True,
            "Failed on get channel name type.",
        )

    def test_set_get_channel_storage(self):
        """Test set and get channel storage"""

        return_var = self.gen.ghs_set_channel_storage_enabled("A", 1, "Enable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set channel storage.",
        )
        return_var, channel_storage = self.gen.ghs_get_channel_storage_enabled(
            "A", 1
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get channel storage.",
        )
        self.assertEqual(
            channel_storage,
            "Enable",
            "Failed to set correct channel storage.",
        )

    def test_set_invalid_channel_storage(self):
        """Test set storage of invalid channel"""

        return_var = self.gen.ghs_set_channel_storage_enabled(
            "Z", 100, "Enable"
        )
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set storage of invalid channel.",
        )

    def test_incorrect_set_channel_storage(self):
        """Test incorrectly set storage of channel"""

        return_var = self.gen.ghs_set_channel_storage_enabled("A", 1, "On")
        self.assertEqual(
            return_var,
            "InvalidDataType",
            "Failed on incorrect setting storage of channel.",
        )

    def test_set_channel_storage_not_idle(self):
        """Test set storage of channel system not idle"""

        return_var = self.gen.ghs_set_storage_location("Local1")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set mainframe as storage location.",
        )

        return_var = self.gen.ghs_start_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to start a recording.",
        )

        return_var = self.gen.ghs_set_channel_storage_enabled("A", 1, "Enable")
        self.assertEqual(
            return_var,
            "SystemNotIdle",
            "Failed on set storage of channel when system not idle.",
        )

        return_var = self.gen.ghs_stop_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to stop recording.",
        )

        time.sleep(2)

    def test_set_channel_storage_disabled_recorder(self):
        """Test set channel storage of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_channel_storage_enabled("A", 1, "Enable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set channel storage of disabled recorder.",
        )

        return_var, channel_storage = self.gen.ghs_get_channel_storage_enabled(
            "A", 1
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get channel storage of disabled recorder.",
        )
        self.assertEqual(
            channel_storage,
            "Enable",
            "Failed to set correct channel storage of disabled recorder.",
        )

    def test_get_invalid_channel_storage(self):
        """Test get storage of invalid channel"""

        return_var = self.gen.ghs_get_channel_storage_enabled("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on set storage of invalid channel.",
        )

    def test_get_channel_storage_disabled_recorder(self):
        """Test get channel storage of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_channel_storage_enabled("A", 1)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get channel storage of disabled recorder.",
        )

    def test_get_channel_storage_valid(self):
        """Test get channel storage and check return value"""

        return_var, enabled = self.gen.ghs_get_channel_storage_enabled("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get channel storage.",
        )
        self.assertEqual(
            enabled in ghsapi.GHSEnableDisable,
            True,
            "Failed on check correct channel storage value.",
        )

    def test_cmd_zeroing(self):
        """Test set zeroing of channel"""

        return_var = self.gen.ghs_cmd_zeroing("A", 1, "Enable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set channel zeroing.",
        )

    def test_cmd_zeroing_invalid_channel(self):
        """Test set zeroing of invalid channel"""

        return_var = self.gen.ghs_cmd_zeroing("Z", 100, "Enable")
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set invalid channel zeroing.",
        )

    def test_cmd_incorrect_zeroing(self):
        """Test set incorrect zeroing of channel"""

        return_var = self.gen.ghs_cmd_zeroing("A", 1, "On")
        self.assertEqual(
            return_var,
            "InvalidDataType",
            "Failed on set incorrect channel zeroing.",
        )

    def test_cmd_zeroing_not_idle(self):
        """Test set zeroing of channel system not idle"""

        return_var = self.gen.ghs_set_storage_location("Local1")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set mainframe as storage location.",
        )

        return_var = self.gen.ghs_start_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to start a recording.",
        )

        return_var = self.gen.ghs_cmd_zeroing("A", 1, "Enable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set zeroing of channel when system not idle.",
        )

        return_var = self.gen.ghs_stop_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to stop recording.",
        )

        time.sleep(2)


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Channel API Functional Test Report",
            report_title="Channel API Functional Test Report",
        )
    )
