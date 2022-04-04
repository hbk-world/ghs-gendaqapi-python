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
        time.sleep(2)
        self.gen.ghs_set_recorder_enabled("A", "Enable")

    # Functions
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
            "Failed on get storage of invalid channel.",
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

    # Analog module
    def test_set_get_trigger_settings(self):
        """Test set and get trigger settings"""

        return_var = self.gen.ghs_set_trigger_settings(
            "A", 1, "Dual", 10.0, 20.0, 30.0, "RisingEdge"
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set trigger settings.",
        )

        (
            return_var,
            trigger_mode,
            primary_level,
            secondary_level,
            hysteresis,
            direction,
        ) = self.gen.ghs_get_trigger_settings("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get trigger settings.",
        )
        self.assertEqual(
            trigger_mode,
            "Dual",
            "Failed to set trigger settings - trigger mode.",
        )
        self.assertEqual(
            primary_level,
            10.0,
            "Failed to set trigger settings - primary level.",
        )
        self.assertEqual(
            secondary_level,
            20.0,
            "Failed to set trigger settings - secondary level.",
        )
        self.assertEqual(
            hysteresis,
            30.0,
            "Failed to set trigger settings - hysteresis.",
        )
        self.assertEqual(
            direction,
            "RisingEdge",
            "Failed to set trigger settings - direction.",
        )

    def test_set_trigger_settings_invalid_channel(self):
        """Test set trigger settings on invalid channel"""

        return_var = self.gen.ghs_set_trigger_settings(
            "Z", 100, "Dual", 10.0, 20.0, 30.0, "RisingEdge"
        )
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set trigger settings on invalid channel.",
        )

    def test_set_trigger_settings_non_analog_channel(self):
        """Test set trigger settings on non analog channel"""

        return_var = self.gen.ghs_set_trigger_settings(
            "A", 25, "Dual", 10.0, 20.0, 30.0, "RisingEdge"
        )
        self.assertEqual(
            return_var,
            "InvalidChannelType",
            "Failed on set trigger settings on non analog channel.",
        )

    def test_set_trigger_settings_disabled_recorder(self):
        """Test set trigger settings of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_trigger_settings(
            "A", 1, "Dual", 20.0, 30.0, 40.0, "RisingEdge"
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set trigger settings of disabled recorder.",
        )

        (
            return_var,
            trigger_mode,
            primary_level,
            secondary_level,
            hysteresis,
            direction,
        ) = self.gen.ghs_get_trigger_settings("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get trigger settings of desabled recorder.",
        )
        self.assertEqual(
            trigger_mode,
            "Dual",
            "Failed to set trigger settings - trigger mode.",
        )
        self.assertEqual(
            primary_level,
            20.0,
            "Failed to set trigger settings - primary level.",
        )
        self.assertEqual(
            secondary_level,
            30.0,
            "Failed to set trigger settings - secondary level.",
        )
        self.assertEqual(
            hysteresis,
            40.0,
            "Failed to set trigger settings - hysteresis.",
        )
        self.assertEqual(
            direction,
            "RisingEdge",
            "Failed to set trigger settings - direction.",
        )

    def test_set_trigger_settings_not_idle(self):
        """Test set trigger settings when system not idle"""

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

        return_var = self.gen.ghs_set_trigger_settings(
            "A", 1, "Dual", 20.0, 30.0, 40.0, "RisingEdge"
        )
        self.assertEqual(
            return_var,
            "SystemNotIdle",
            "Failed on set trigger settings when system not idle.",
        )

        return_var = self.gen.ghs_stop_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to stop recording.",
        )

        time.sleep(2)

    def test_get_invalid_trigger_settings(self):
        """Test get trigger settings of invalid channel"""

        return_var = self.gen.ghs_get_trigger_settings("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get trigger settings of invalid channel.",
        )

    def test_get_trigger_settings_disabled_recorder(self):
        """Test get trigger settings of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_trigger_settings("A", 1)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get trigger settings of disabled recorder.",
        )

    def test_get_trigger_settings_non_analog(self):
        """Test get trigger settings of non analog channel"""

        return_var = self.gen.ghs_get_trigger_settings("A", 25)
        self.assertEqual(
            return_var[0],
            "InvalidChannelType",
            "Failed on get trigger settings of non analog channel.",
        )

    def test_get_trigger_settings_valid(self):
        """Test get trigger settings and check return value"""

        (
            return_var,
            trigger_mode,
            primary_level,
            secondary_level,
            hysteresis,
            direction,
        ) = self.gen.ghs_get_trigger_settings("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get trigger settings.",
        )
        self.assertEqual(
            trigger_mode in ghsapi.GHSTriggerMode,
            True,
            "Failed on validate trigger settings - trigger mode",
        )
        self.assertEqual(
            direction in ghsapi.GHSDirection,
            True,
            "Failed on validate trigger settings - direction",
        )
        self.assertEqual(
            isinstance(primary_level, float)
            and isinstance(secondary_level, float)
            and isinstance(hysteresis, float),
            True,
            "Failed on validate trigger settings.",
        )

    def test_set_get_signal_coupling(self):
        """Test set and get signal coupling"""

        return_var = self.gen.ghs_set_signal_coupling("A", 1, "DC")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set signal coupling.",
        )

        return_var, signal_coupling = self.gen.ghs_get_signal_coupling("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get signal coupling.",
        )
        self.assertEqual(
            signal_coupling,
            "DC",
            "Failed to set signal coupling.",
        )

    def test_set_signal_coupling_invalid_channel(self):
        """Test set signal coupling on invalid channel"""

        return_var = self.gen.ghs_set_signal_coupling("Z", 100, "DC")
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set signal coupling on invalid channel.",
        )

    def test_set_signal_coupling_non_analog_channel(self):
        """Test set signal coupling on non analog channel"""

        return_var = self.gen.ghs_set_signal_coupling("A", 25, "DC")
        self.assertEqual(
            return_var,
            "InvalidChannelType",
            "Failed on set signal coupling on non analog channel.",
        )

    def test_set_signal_coupling_disabled_recorder(self):
        """Test set signal coupling of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_signal_coupling("A", 1, "DC")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set signal coupling of disabled recorder.",
        )

        return_var, signal_coupling = self.gen.ghs_get_signal_coupling("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get signal coupling of disabled recorder.",
        )
        self.assertEqual(
            signal_coupling,
            "DC",
            "Failed to set signal coupling.",
        )

    def test_set_signal_coupling_not_supported(self):
        """Test set signal coupling with not supported mode"""

        return_var = self.gen.ghs_set_signal_coupling("A", 1, "Charge")
        self.assertEqual(
            return_var,
            "Adapted",
            "Failed on set signal coupling with not supported mode.",
        )

    def test_get_invalid_signal_coupling(self):
        """Test get signal coupling of invalid channel"""

        return_var = self.gen.ghs_get_signal_coupling("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get signal coupling of invalid channel.",
        )

    def test_get_signal_coupling_disabled_recorder(self):
        """Test get signal coupling of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_signal_coupling("A", 1)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get signal coupling of disabled recorder.",
        )

    def test_get_signal_coupling_non_analog(self):
        """Test get signal coupling of non analog channel"""

        return_var = self.gen.ghs_get_signal_coupling("A", 25)
        self.assertEqual(
            return_var[0],
            "InvalidChannelType",
            "Failed on get signal coupling of non analog channel.",
        )

    def test_set_get_input_coupling(self):
        """Test set and get input coupling"""

        return_var = self.gen.ghs_set_input_coupling(
            "A", 1, "SingleEndedPositive"
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set input coupling.",
        )

        return_var, input_coupling = self.gen.ghs_get_input_coupling("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get input coupling.",
        )
        self.assertEqual(
            input_coupling,
            "SingleEndedPositive",
            "Failed to set input coupling.",
        )

    def test_set_input_coupling_invalid_channel(self):
        """Test set input coupling on invalid channel"""

        return_var = self.gen.ghs_set_input_coupling(
            "Z", 100, "SingleEndedPositive"
        )
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set input coupling on invalid channel.",
        )

    def test_set_input_coupling_non_analog_channel(self):
        """Test set input coupling on non analog channel"""

        return_var = self.gen.ghs_set_input_coupling(
            "A", 25, "SingleEndedPositive"
        )
        self.assertEqual(
            return_var,
            "InvalidChannelType",
            "Failed on set input coupling on non analog channel.",
        )

    def test_set_input_coupling_disabled_recorder(self):
        """Test set input coupling of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_input_coupling(
            "A", 1, "SingleEndedPositive"
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set input coupling of disabled recorder.",
        )

        return_var, input_coupling = self.gen.ghs_get_input_coupling("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get input coupling of disabled recorder.",
        )
        self.assertEqual(
            input_coupling,
            "SingleEndedPositive",
            "Failed to set input coupling.",
        )

    def test_set_input_coupling_not_supported(self):
        """Test set input coupling with not supported mode"""

        return_var = self.gen.ghs_set_input_coupling(
            "A", 1, "FloatingDifferential"
        )
        self.assertEqual(
            return_var,
            "Adapted",
            "Failed on set input coupling with not supported mode.",
        )

    def test_set_input_coupling_not_idle(self):
        """Test set input coupling when system not idle"""

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

        return_var = self.gen.ghs_set_input_coupling(
            "A", 1, "SingleEndedPositive"
        )
        self.assertEqual(
            return_var,
            "SystemNotIdle",
            "Failed on set trigger settings when system not idle.",
        )

        return_var = self.gen.ghs_stop_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to stop recording.",
        )

        time.sleep(2)

    def test_get_invalid_input_coupling(self):
        """Test get input coupling of invalid channel"""

        return_var = self.gen.ghs_get_input_coupling("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get input coupling of invalid channel.",
        )

    def test_get_input_coupling_disabled_recorder(self):
        """Test get input coupling of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_input_coupling("A", 1)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get input coupling of disabled recorder.",
        )

    def test_get_input_coupling_non_analog(self):
        """Test get input coupling of non analog channel"""

        return_var = self.gen.ghs_get_input_coupling("A", 25)
        self.assertEqual(
            return_var[0],
            "InvalidChannelType",
            "Failed on get input coupling of non analog channel.",
        )

    def test_set_get_span_offset(self):
        """Test set and get span and offset"""

        return_var = self.gen.ghs_set_span_and_offset("A", 1, 10.0, 20.0)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set span and offset.",
        )

        return_var, span, offset = self.gen.ghs_get_span_and_offset("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get span and offset.",
        )
        self.assertEqual(
            span,
            10.0,
            "Failed to set span.",
        )
        self.assertEqual(
            offset,
            20.0,
            "Failed to set offset.",
        )

    def test_set_span_offset_invalid_channel(self):
        """Test set span and offset on invalid channel"""

        return_var = self.gen.ghs_set_span_and_offset("Z", 100, 10.0, 20.0)
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set span and offset on invalid channel.",
        )

    def test_set_span_offset_non_analog_channel(self):
        """Test set span and offset on non analog channel"""

        return_var = self.gen.ghs_set_span_and_offset("A", 25, 10.0, 20.0)
        self.assertEqual(
            return_var,
            "InvalidChannelType",
            "Failed on set span and offset on non analog channel.",
        )

    def test_set_span_offset_disabled_recorder(self):
        """Test set span and offset of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_span_and_offset("A", 1, 10.0, 20.0)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set span and offset of disabled recorder.",
        )

        return_var, span, offset = self.gen.ghs_get_span_and_offset("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get span and offset on disabled recorder.",
        )
        self.assertEqual(
            span,
            10.0,
            "Failed to set span.",
        )
        self.assertEqual(
            offset,
            20.0,
            "Failed to set offset.",
        )

    def test_get_invalid_span_offset(self):
        """Test get span offset of invalid channel"""

        return_var = self.gen.ghs_get_span_and_offset("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get span offset of invalid channel.",
        )

    def test_get_span_offset_disabled_recorder(self):
        """Test get span offset of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_span_and_offset("A", 1)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get span and offset of disabled recorder.",
        )

    def test_get_span_offset_non_analog(self):
        """Test get span and offset of non analog channel"""

        return_var = self.gen.ghs_get_span_and_offset("A", 25)
        self.assertEqual(
            return_var[0],
            "InvalidChannelType",
            "Failed on get span and offset of non analog channel.",
        )

    def test_set_get_filter_frequency(self):
        """Test set and get filter type and frequency"""

        return_var = self.gen.ghs_set_filter_type_and_frequency(
            "A", 1, "Bessel_AA", 32000000.0
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set filter type and frequency.",
        )

        (
            return_var,
            filter_type,
            frequency,
        ) = self.gen.ghs_get_filter_type_and_frequency("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get filter type and frequency.",
        )
        self.assertEqual(
            filter_type,
            "Bessel_AA",
            "Failed to set filter type.",
        )
        self.assertEqual(
            frequency,
            32000000.0,
            "Failed to set frequency.",
        )

    def test_set_filter_frequency_invalid_channel(self):
        """Test set filter type and frequency on invalid channel"""

        return_var = self.gen.ghs_set_filter_type_and_frequency(
            "Z", 100, "Bessel_AA", 32000000.0
        )
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set filter type and frequency on invalid channel.",
        )

    def test_set_filter_frequency_non_analog_channel(self):
        """Test set filter type and frequency on non analog channel"""

        return_var = self.gen.ghs_set_filter_type_and_frequency(
            "A", 25, "Bessel_AA", 32000000.0
        )
        self.assertEqual(
            return_var,
            "InvalidChannelType",
            "Failed on set filter type and frequency on non analog channel.",
        )

    def test_set_filter_frequency_disabled_recorder(self):
        """Test set filter type and frequency of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_filter_type_and_frequency(
            "A", 1, "Bessel_AA", 32000000.0
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set filter type and frequency of disabled recorder.",
        )

        (
            return_var,
            filter_type,
            frequency,
        ) = self.gen.ghs_get_filter_type_and_frequency("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get filter type and frequency of disabled recorder.",
        )
        self.assertEqual(
            filter_type,
            "Bessel_AA",
            "Failed to set filter type.",
        )
        self.assertEqual(
            frequency,
            32000000.0,
            "Failed to set frequency.",
        )

    def test_get_invalid_filter_frequency(self):
        """Test get filter type and frequency of invalid channel"""

        return_var = self.gen.ghs_get_filter_type_and_frequency("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get filter type and frequency of invalid channel.",
        )

    def test_get_filter_frequency_disabled_recorder(self):
        """Test get filter type and frequency of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_filter_type_and_frequency("A", 1)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get filter type and frequency of disabled recorder.",
        )

    def test_get_filter_frequency_non_analog(self):
        """Test get filter type and frequency of non analog channel"""

        return_var = self.gen.ghs_get_filter_type_and_frequency("A", 25)
        self.assertEqual(
            return_var[0],
            "InvalidChannelType",
            "Failed on get filter type and frequency of non analog channel.",
        )

    def test_set_get_excitation(self):
        """Test set and get excitation type and value"""

        return_var = self.gen.ghs_set_excitation("A", 1, "Voltage", 10.0)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set excitation type and value.",
        )

        (
            return_var,
            excitation_type,
            excitation_value,
        ) = self.gen.ghs_get_excitation("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get excitation type and value.",
        )
        self.assertEqual(
            excitation_type,
            "Voltage",
            "Failed to set excitation type.",
        )
        self.assertEqual(
            excitation_value,
            10.0,
            "Failed to set excitation value.",
        )

    def test_set_excitation_invalid_channel(self):
        """Test set excitation type and value on invalid channel"""

        return_var = self.gen.ghs_set_excitation("Z", 100, "Voltage", 10.0)
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set excitation type and value on invalid channel.",
        )

    def test_set_excitation_non_analog_channel(self):
        """Test set excitation type and value on non analog channel"""

        return_var = self.gen.ghs_set_excitation("A", 25, "Voltage", 10.0)
        self.assertEqual(
            return_var,
            "InvalidChannelType",
            "Failed on set excitation type and value on non analog channel.",
        )

    def test_set_excitation_disabled_recorder(self):
        """Test set excitation type and value of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_excitation("A", 1, "Voltage", 10.0)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set excitation type and value of disabled recorder.",
        )

        (
            return_var,
            excitation_type,
            excitation_value,
        ) = self.gen.ghs_get_excitation("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get excitation type and value of disabled recorder.",
        )
        self.assertEqual(
            excitation_type,
            "Voltage",
            "Failed to set excitation type.",
        )
        self.assertEqual(
            excitation_value,
            10.0,
            "Failed to set excitation value.",
        )

    def test_set_excitation_not_supported(self):
        """Test set excitation type and value with not supported value"""

        return_var = self.gen.ghs_set_excitation("A", 1, "Voltage", 15.0)
        self.assertEqual(
            return_var,
            "Adapted",
            "Failed on set excitation type and value with not supported type.",
        )

    def test_get_invalid_excitation(self):
        """Test get excitation type and value of invalid channel"""

        return_var = self.gen.ghs_get_excitation("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get excitation type and value of invalid channel.",
        )

    def test_get_excitation_disabled_recorder(self):
        """Test get excitation type and value of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_excitation("A", 1)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get excitation type and value of disabled recorder.",
        )

    def test_get_excitation_non_analog(self):
        """Test get excitation type and value of non analog channel"""

        return_var = self.gen.ghs_get_excitation("A", 25)
        self.assertEqual(
            return_var[0],
            "InvalidChannelType",
            "Failed on get excitation type and value of non analog channel.",
        )

    def test_set_get_amplifier_mode(self):
        """Test set and get amplifier mode"""

        return_var = self.gen.ghs_set_amplifier_mode("A", 1, "Basic")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set amplifier mode.",
        )

        (
            return_var,
            amplifier_mode,
        ) = self.gen.ghs_get_amplifier_mode("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get amplifier mode.",
        )
        self.assertEqual(
            amplifier_mode,
            "Basic",
            "Failed to set amplifier mode.",
        )

    def test_set_amplifier_mode_invalid_channel(self):
        """Test set amplifier mode on invalid channel"""

        return_var = self.gen.ghs_set_amplifier_mode("Z", 100, "Basic")
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set amplifier mode on invalid channel.",
        )

    def test_set_amplifier_mode_non_analog_channel(self):
        """Test set amplifier mode on non analog channel"""

        return_var = self.gen.ghs_set_amplifier_mode("A", 25, "Basic")
        self.assertEqual(
            return_var,
            "InvalidChannelType",
            "Failed on set amplifier mode on non analog channel.",
        )

    def test_set_amplifier_mode_disabled_recorder(self):
        """Test set amplifier mode of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_amplifier_mode("A", 1, "Basic")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set amplifier mode of disabled recorder.",
        )

        (
            return_var,
            amplifier_mode,
        ) = self.gen.ghs_get_amplifier_mode("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get amplifier mode of disabled recorder.",
        )
        self.assertEqual(
            amplifier_mode,
            "Basic",
            "Failed to set amplifier mode.",
        )

    def test_get_invalid_amplifier_mode(self):
        """Test get amplifier mode of invalid channel"""

        return_var = self.gen.ghs_get_amplifier_mode("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get amplifier mode of invalid channel.",
        )

    def test_get_amplifier_mode_disabled_recorder(self):
        """Test get amplifier mode of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_amplifier_mode("A", 1)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get amplifier mode of disabled recorder.",
        )

    def test_get_amplifier_mode_non_analog(self):
        """Test get amplifier mode of non analog channel"""

        return_var = self.gen.ghs_get_amplifier_mode("A", 25)
        self.assertEqual(
            return_var[0],
            "InvalidChannelType",
            "Failed on get amplifier mode of non analog channel.",
        )

    def test_set_get_technical_units(self):
        """Test set and get technical units, unit multiplier and unit offset"""

        return_var = self.gen.ghs_set_technical_units(
            "A", 1, "KGS", 10.0, 20.0
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set technical units, unit multiplier and unit offset.",
        )

        (
            return_var,
            units,
            multiplier,
            offset,
        ) = self.gen.ghs_get_technical_units("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get technical units, unit multiplier and unit offset.",
        )
        self.assertEqual(
            units,
            "KGS",
            "Failed to set technical units.",
        )
        self.assertEqual(
            multiplier,
            10.0,
            "Failed to set unit multiplier.",
        )
        self.assertEqual(
            offset,
            20.0,
            "Failed to set unit offset.",
        )

    def test_set_technical_units_invalid_channel(self):
        """Test set technical units, unit multiplier and unit offset on invalid channel"""

        return_var = self.gen.ghs_set_technical_units(
            "Z", 100, "KGS", 10.0, 20.0
        )
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set technical units, unit multiplier and unit offset on invalid channel.",
        )

    def test_set_technical_units_non_analog_channel(self):
        """Test set technical units, unit multiplier and unit offset on non analog channel"""

        return_var = self.gen.ghs_set_technical_units(
            "A", 25, "KGS", 10.0, 20.0
        )
        self.assertEqual(
            return_var,
            "InvalidChannelType",
            "Failed on set technical units, unit multiplier and unit offset on non analog channel.",
        )

    def test_set_technical_units_disabled_recorder(self):
        """Test set technical units, unit multiplier and unit offset of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_technical_units(
            "A", 1, "KGS", 10.0, 20.0
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set technical units, unit multiplier and unit offset of disabled recorder.",
        )

        (
            return_var,
            units,
            multiplier,
            offset,
        ) = self.gen.ghs_get_technical_units("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get technical units, unit multiplier and unit offset of disabled recorder.",
        )
        self.assertEqual(
            units,
            "KGS",
            "Failed to set technical units.",
        )
        self.assertEqual(
            multiplier,
            10.0,
            "Failed to set unit multiplier.",
        )
        self.assertEqual(
            offset,
            20.0,
            "Failed to set unit offset.",
        )

    def test_get_invalid_technical_units(self):
        """Test get technical units, unit multiplier and unit offset of invalid channel"""

        return_var = self.gen.ghs_get_technical_units("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get technical units, unit multiplier and unit offset of invalid channel.",
        )

    def test_get_technical_units_disabled_recorder(self):
        """Test get technical units, unit multiplier and unit offset of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_technical_units("A", 1)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get technical units, unit multiplier and unit offset of disabled recorder.",
        )

    def test_get_technical_units_non_analog(self):
        """Test get technical units, unit multiplier and unit offset of non analog channel"""

        return_var = self.gen.ghs_get_technical_units("A", 25)
        self.assertEqual(
            return_var[0],
            "InvalidChannelType",
            "Failed on get technical units, unit multiplier and unit offset of non analog channel.",
        )

    def test_set_get_auto_range(self):
        """Test set and get auto range enable and time settings"""

        return_var = self.gen.ghs_set_auto_range("A", 1, "Enable", 10.0)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set auto range enable and time settings.",
        )

        (
            return_var,
            auto_range_enabled,
            auto_range_time,
        ) = self.gen.ghs_get_auto_range("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get auto range enable and time settings.",
        )
        self.assertEqual(
            auto_range_enabled,
            "Enable",
            "Failed to set auto range enable.",
        )
        self.assertEqual(
            auto_range_time,
            10.0,
            "Failed to set time settings.",
        )

    def test_set_auto_range_invalid_channel(self):
        """Test set auto range enable and time settings on invalid channel"""

        return_var = self.gen.ghs_set_auto_range("Z", 100, "Enable", 10.0)
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set auto range enable and time settings on invalid channel.",
        )

    def test_set_auto_range_non_analog_channel(self):
        """Test set auto range enable and time settings on non analog channel"""

        return_var = self.gen.ghs_set_auto_range("A", 25, "Enable", 10.0)
        self.assertEqual(
            return_var,
            "InvalidChannelType",
            "Failed on set auto range enable and time settings on non analog channel.",
        )

    def test_set_auto_range_disabled_recorder(self):
        """Test set auto range enable and time settings of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_auto_range("A", 1, "Enable", 10.0)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set auto range enable and time settings of disabled recorder.",
        )

        (
            return_var,
            auto_range_enabled,
            auto_range_time,
        ) = self.gen.ghs_get_auto_range("A", 1)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get auto range enable and time settings of disabled recorder.",
        )
        self.assertEqual(
            auto_range_enabled,
            "Enable",
            "Failed to set auto range enable.",
        )
        self.assertEqual(
            auto_range_time,
            10.0,
            "Failed to set time settings.",
        )

    def test_get_invalid_auto_range(self):
        """Test get auto range enable and time settings of invalid channel"""

        return_var = self.gen.ghs_get_auto_range("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get auto range enable and time settings of invalid channel.",
        )

    def test_get_auto_range_disabled_recorder(self):
        """Test get auto range enable and time settings of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_auto_range("A", 1)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get auto range enable and time settings of disabled recorder.",
        )

    def test_get_auto_range_non_analog(self):
        """Test get auto range enable and time settings of non analog channel"""

        return_var = self.gen.ghs_get_auto_range("A", 25)
        self.assertEqual(
            return_var[0],
            "InvalidChannelType",
            "Failed on get auto range enable and time settings of non analog channel.",
        )

    def test_cmd_auto_range_now(self):
        """Test command a single shot for auto range"""

        return_var = self.gen.ghs_cmd_auto_range_now("A", 1, 20.0)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on command a single shot for auto range.",
        )

    def test_cmd_auto_range_now_invalid_channel(self):
        """Test command a single shot for auto range on invalid channel"""

        return_var = self.gen.ghs_cmd_auto_range_now("Z", 100, 20.0)
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on command a single shot for auto range on invalid channel.",
        )

    def test_cmd_auto_range_now_non_analog_channel(self):
        """Test command a single shot for auto range on non analog channel"""

        return_var = self.gen.ghs_cmd_auto_range_now("A", 25, 20.0)
        self.assertEqual(
            return_var,
            "InvalidChannelType",
            "Failed on command a single shot for auto range on non analog channel.",
        )

    def test_get_channel_cal_info(self):
        """Test to get calibration information for an analog channel."""

        return_var = self.gen.ghs_get_channel_cal_info("A", 1)
        result_type = (
            return_var[0] == "OK"
            and isinstance(return_var[1], str)
            and isinstance(return_var[2], str)
            and isinstance(return_var[3], str)
            and isinstance(return_var[4], str)
            and isinstance(return_var[5], str)
            and isinstance(return_var[6], str)
        )
        self.assertEqual(
            result_type,
            True,
            "Failed to get calibration information.",
        )

    # Timer/Counter Module
    ## NOTE: Enter valid timer/counter channel slot ID and index
    def test_set_get_gate_mode(self):
        """Test set and get timer/counter mode"""

        return_var = self.gen.ghs_set_timer_counter_mode(
            "A", 25, "CountQuadrature"
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set timer/counter mode.",
        )

        (
            return_var,
            mode,
        ) = self.gen.ghs_get_timer_counter_mode("A", 25)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get timer/counter mode.",
        )
        self.assertEqual(
            mode,
            "CountQuadrature",
            "Failed to set timer/counter mode.",
        )

    def test_set_gate_mode_invalid_channel(self):
        """Test set timer/counter mode on invalid channel"""

        return_var = self.gen.ghs_set_timer_counter_mode(
            "Z", 100, "CountQuadrature"
        )
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set timer/counter mode on invalid channel.",
        )

    def test_set_gate_mode_non_timer_counter_channel(self):
        """Test set timer/counter mode on non timer/counter channel"""

        return_var = self.gen.ghs_set_timer_counter_mode(
            "A", 1, "CountQuadrature"
        )
        self.assertEqual(
            return_var,
            "InvalidChannelType",
            "Failed on set timer/counter mode on non timer/counter channel.",
        )

    def test_set_gate_mode_disabled_recorder(self):
        """Test set timer/counter mode of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_timer_counter_mode(
            "A", 25, "CountQuadrature"
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set timer/counter mode of disabled recorder.",
        )

        (
            return_var,
            mode,
        ) = self.gen.ghs_get_timer_counter_mode("A", 25)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get timer/counter mode of disabled recorder.",
        )
        self.assertEqual(
            mode,
            "CountQuadrature",
            "Failed to set timer/counter mode.",
        )

    def test_get_invalid_gate_mode(self):
        """Test get timer/counter mode of invalid channel"""

        return_var = self.gen.ghs_get_timer_counter_mode("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get timer/counter mode of invalid channel.",
        )

    def test_get_gate_mode_disabled_recorder(self):
        """Test get timer/counter mode of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_timer_counter_mode("A", 25)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get timer/counter mode of disabled recorder.",
        )

    def test_get_gate_mode_non_timer_counter(self):
        """Test get timer/counter mode of non timer/counter channel"""

        return_var = self.gen.ghs_get_timer_counter_mode("A", 1)
        self.assertEqual(
            return_var[0],
            "InvalidChannelType",
            "Failed on get timer/counter mode of non timer/counter channel.",
        )

    def test_set_get_gate_time(self):
        """Test set and get gate time for a timer/counter channel"""

        return_var = self.gen.ghs_set_timer_counter_gate_time("A", 25, 10.0)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set gate time for a timer/counter channel.",
        )

        (
            return_var,
            gate_time,
        ) = self.gen.ghs_get_timer_counter_gate_time("A", 25)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get gate time for a timer/counter channel.",
        )
        self.assertEqual(
            gate_time,
            10.0,
            "Failed to set time gate time.",
        )

    def test_gate_time_invalid_channel(self):
        """Test set gate time for a timer/counter channel on invalid channel"""

        return_var = self.gen.ghs_set_timer_counter_gate_time("Z", 100, 10.0)
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set gate time for a timer/counter channel on invalid channel.",
        )

    def test_set_gate_time_non_timer_counter_channel(self):
        """Test set gate time for a timer/counter channel on non timer/counter channel"""

        return_var = self.gen.ghs_set_timer_counter_gate_time("A", 1, 10.0)
        self.assertEqual(
            return_var,
            "InvalidChannelType",
            "Failed on set gate time for a timer/counter channel on non timer/counter channel.",
        )

    def test_set_gate_time_disabled_recorder(self):
        """Test set gate time for a timer/counter channel of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_timer_counter_gate_time("A", 25, 10.0)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set gate time for a timer/counter channel of disabled recorder.",
        )

        (
            return_var,
            gate_time,
        ) = self.gen.ghs_get_timer_counter_gate_time("A", 25)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get gate time for a timer/counter channel of disabled recorder.",
        )
        self.assertEqual(
            gate_time,
            10.0,
            "Failed to set gate time.",
        )

    def test_get_invalid_gate_time(self):
        """Test get gate time for a timer/counter channel of invalid channel"""

        return_var = self.gen.ghs_get_timer_counter_gate_time("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get gate time for a timer/counter channel of invalid channel.",
        )

    def test_get_gate_time_disabled_recorder(self):
        """Test get gate time for a timer/counter channel of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_timer_counter_gate_time("A", 25)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get gate time for a timer/counter channel of disabled recorder.",
        )

    def test_get_gate_time_non_timer_counter(self):
        """Test get gate time for a timer/counter channel of non timer/counter channel"""

        return_var = self.gen.ghs_get_timer_counter_gate_time("A", 1)
        self.assertEqual(
            return_var[0],
            "InvalidChannelType",
            "Failed on get gate time for a timer/counter channel of non analog channel.",
        )

    def test_set_get_timer_counter_range(self):
        """Test set and get range for a timer/counter channel"""

        return_var = self.gen.ghs_set_timer_counter_range("A", 25, 10.0, 20.0)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set range for a timer/counter channel.",
        )

        (
            return_var,
            lower,
            upper,
        ) = self.gen.ghs_get_timer_counter_range("A", 25)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get range for a timer/counter channel.",
        )
        self.assertEqual(
            lower,
            10.0,
            "Failed to set lower range.",
        )
        self.assertEqual(
            upper,
            20.0,
            "Failed to set upper range.",
        )

    def test_set_timer_counter_range_invalid_channel(self):
        """Test set range for a timer/counter on invalid channel"""

        return_var = self.gen.ghs_set_timer_counter_range("Z", 100, 10.0, 20.0)
        self.assertEqual(
            return_var,
            "InvalidSlotID",
            "Failed on set range for a timer/counter on invalid channel.",
        )

    def test_set_range_non_timer_counter_channel(self):
        """Test set range on non timer/counter channel"""

        return_var = self.gen.ghs_set_timer_counter_range("A", 1, 10.0, 20.0)
        self.assertEqual(
            return_var,
            "InvalidChannelType",
            "Failed on set range on non timer/counters channel.",
        )

    def test_set_timer_counter_range_disabled_recorder(self):
        """Test set timer/counter range of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_set_timer_counter_range("A", 25, 10.0, 20.0)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set timer/counter range of disabled recorder.",
        )

        (
            return_var,
            lower,
            upper,
        ) = self.gen.ghs_get_timer_counter_range("A", 25)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get timer/counter range of disabled recorder.",
        )
        self.assertEqual(
            lower,
            10.0,
            "Failed to set lower range.",
        )
        self.assertEqual(
            upper,
            20.0,
            "Failed to set upper range.",
        )

    def test_get_invalid_timer_counter_range(self):
        """Test get timer/counter range of invalid channel"""

        return_var = self.gen.ghs_get_timer_counter_range("Z", 100)
        self.assertEqual(
            return_var[0],
            "InvalidSlotID",
            "Failed on get timer/counter range of invalid channel.",
        )

    def test_get_timer_counter_range_disabled_recorder(self):
        """Test get timer/counter range of disabled recorder"""

        return_var = self.gen.ghs_set_recorder_enabled("A", "Disable")
        self.assertEqual(
            return_var,
            "OK",
            "Failed to disable recorder.",
        )

        return_var = self.gen.ghs_get_timer_counter_range("A", 25)
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get timer/counter range of disabled recorder.",
        )

    def test_get_range_non_timer_counter(self):
        """Test get range of non timer/counter channel"""

        return_var = self.gen.ghs_get_timer_counter_range("A", 1)
        self.assertEqual(
            return_var[0],
            "InvalidChannelType",
            "Failed on get range of non timer/counter channel.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Channel API Functional Test Report",
            report_title="Channel API Functional Test Report",
        )
    )
