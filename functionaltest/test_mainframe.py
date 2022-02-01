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

"""Mainframe API functional test."""

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


class TestMainframe(unittest.TestCase):
    """Mainframe API functional test."""

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
        self.gen.ghs_stop_preview()
        self.gen.ghs_stop_recording()
        time.sleep(2)

    def test_identify(self):
        """Test to enable or disable the identification sound."""

        self.assertEqual(
            self.gen.ghs_identify(True),
            "OK",
            "Failed to enable the identification sound.",
        )

        self.assertEqual(
            self.gen.ghs_identify(False),
            "OK",
            "Failed to disable the identification sound.",
        )

    def test_get_mainframe_info(self):
        """Test to get mainframe information."""

        return_var = self.gen.ghs_get_mainframe_info()
        result_type = (
            return_var[0] == "OK"
            and isinstance(return_var[1], str)
            and isinstance(return_var[2], str)
            and isinstance(return_var[3], str)
        )
        self.assertEqual(
            result_type,
            True,
            "Failed to get mainframe information.",
        )

    def test_get_disk_space(self):
        """Test to get disk space."""

        return_var = self.gen.ghs_get_disk_space()
        result_type = (
            return_var[0] == "OK"
            and isinstance(return_var[1], float)
            and isinstance(return_var[2], float)
        )
        self.assertEqual(
            result_type,
            True,
            "Failed to get disk space.",
        )

    def test_total_available_disk_space(self):
        """Test available disk space less than total."""

        return_var = self.gen.ghs_get_disk_space()
        self.assertEqual(
            return_var[1] >= return_var[2] and return_var[0] == "OK",
            True,
            "Failed available disk space more than total.",
        )

    def test_decrease_available_disk_space(self):
        """Test if available disk space decreases."""

        return_var = self.gen.ghs_get_disk_space()
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get disk space.",
        )
        available_1 = return_var[2]

        return_var = self.gen.ghs_start_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on config recording.",
        )
        time.sleep(3)
        return_var = self.gen.ghs_stop_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on config recording.",
        )
        time.sleep(2)

        return_var = self.gen.ghs_get_disk_space()
        self.assertEqual(
            return_var[0],
            "OK",
            "Failed on get disk space.",
        )
        available_2 = return_var[2]

        self.assertEqual(
            available_1 > available_2,
            True,
            "Failed available disk space change.",
        )

    # TODO: One possible functional test for get_disk_space is to see
    # if an error is returned when Remote Storage is selected (will be
    # possible when set_storage_location is done)

    def test_sync_status(self):
        """Test mainframe sync status."""

        return_var, sync_status = self.gen.ghs_get_sync_status()
        self.assertEqual(
            sync_status in ghsapi.GHSSyncStatus and return_var == "OK",
            True,
            "Failed on mainframe sync status.",
        )

    def test_get_slot_count(self):
        """Test to get slot count."""

        return_var = self.gen.ghs_get_slot_count()
        self.assertEqual(
            isinstance(return_var[1], int) and return_var[0] == "OK",
            True,
            "Failed to get slot count.",
        )

    # TODO: One possible test when set_recorder_enabled is implemented
    # is to see if get_slot_count returns a different number if some
    # recorders are disabled

    def test_get_user_mode(self):
        """Test get user mode."""

        return_var, user_mode = self.gen.ghs_get_user_mode()
        self.assertEqual(
            user_mode in ghsapi.GHSUserMode and return_var == "OK",
            True,
            "Failed on get user mode.",
        )

    def test_set_user_mode(self):
        """Test set user mode."""

        return_var = self.gen.ghs_set_user_mode("Dual")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set user mode.",
        )
        time.sleep(1)

        return_var, user_mode = self.gen.ghs_get_user_mode()
        self.assertEqual(
            user_mode,
            "Dual",
            "Failed on get user mode.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get user mode.",
        )

    def test_set_user_mode_recording(self):
        """Test set user mode when recording."""

        return_var = self.gen.ghs_start_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on config recording.",
        )

        return_var = self.gen.ghs_set_user_mode("Dual")
        self.assertEqual(
            return_var,
            "SystemNotIdle",
            "Failed set user mode when recording.",
        )

    def test_set_user_mode_preview(self):
        """Test set user mode when in preview."""

        return_var = self.gen.ghs_start_preview()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on config preview.",
        )

        return_var = self.gen.ghs_set_user_mode("Dual")
        self.assertEqual(
            return_var,
            "SystemNotIdle",
            "Failed set user mode when in preview.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Mainframe API Functional Test Report",
            report_title="Mainframe API Functional Test Report",
        )
    )
