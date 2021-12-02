"""Mainframe API functional test."""

import os
import sys
import time
import unittest

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src import ghsapi

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
        pass

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
            return_var[1] >= return_var[2],
            True,
            "Failed available disk space more than total.",
        )

    def test_decrease_available_disk_space(self):
        """Test if available disk space decreases."""

        return_var = self.gen.ghs_get_disk_space()
        available_1 = return_var[2]

        self.gen.ghs_start_recording()
        time.sleep(3)
        self.gen.ghs_stop_recording()
        time.sleep(2)

        return_var = self.gen.ghs_get_disk_space()
        available_2 = return_var[2]

        self.assertEqual(
            available_1 > available_2,
            True,
            "Failed available disk space change.",
        )

    def test_sync_status(self):
        """Test mainframe sync status."""

        _, sync_status = self.gen.ghs_get_sync_status()
        self.assertEqual(
            sync_status in ghsapi.GHSSyncStatus,
            True,
            "Failed on mainframe sync status.",
        )

    def test_get_slot_count(self):
        """Test to get slot count."""

        return_var = self.gen.ghs_get_slot_count()
        self.assertEqual(
            isinstance(return_var[1], int),
            True,
            "Failed to get slot count.",
        )

    def test_get_user_mode(self):
        """Test get user mode."""

        _, user_mode = self.gen.ghs_get_user_mode()
        self.assertEqual(
            user_mode in ghsapi.GHSUserMode,
            True,
            "Failed on get user mode.",
        )

    def test_set_user_mode(self):
        """Test set user mode."""

        self.gen.ghs_set_user_mode("Dual")
        time.sleep(1)

        _, user_mode = self.gen.ghs_get_user_mode()
        self.assertEqual(
            user_mode,
            "Dual",
            "Failed on set user mode.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Mainframe API Functional Test Report",
            report_title="Mainframe API Functional Test Report",
        )
    )
