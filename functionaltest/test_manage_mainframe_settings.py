"""Manage mainframe settings API functional test."""

import os
import sys
import unittest

import HtmlTestRunner

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

sys.path.append(parentdir)

from src import ghsapi

IP_ADDRESS = "localhost"
PORT_NO = 8006


class TestManageMainframeSettings(unittest.TestCase):
    """Manage mainframe settings API functional test."""

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

    def test_persist_current_settings(self):
        """Test copy of active settings to boot settings."""

        return_var = self.gen.ghs_persist_current_settings()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to persist current settings.",
        )

    def test_apply_persisted_settings(self):
        """Test copy of boot settings to active settings."""

        return_var = self.gen.ghs_apply_persisted_settings()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to apply persisted settings.",
        )

    def test_set_get_current_settings(self):
        """Test to set then get current settings."""

        return_var = self.gen.ghs_set_high_low_rate_storage_enabled(
            "SyncChannels", "A", "Enable", "Enable"
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set high low storage enabled.",
        )

        return_var, high, low = self.gen.ghs_get_high_low_rate_storage_enabled(
            "SyncChannels", "A"
        )
        self.assertEqual(
            high,
            "Enable",
            "Failed on get high low storage enabled.",
        )
        self.assertEqual(
            low,
            "Enable",
            "Failed on get high low storage enabled.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get high low storage enabled.",
        )

        (
            return_var,
            blob_enable,
            blob_size_enable,
        ) = self.gen.ghs_get_current_settings()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to get current settings.",
        )

        return_var = self.gen.ghs_set_high_low_rate_storage_enabled(
            "SyncChannels", "A", "Disable", "Disable"
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set high low storage disabled.",
        )

        return_var, high, low = self.gen.ghs_get_high_low_rate_storage_enabled(
            "SyncChannels", "A"
        )
        self.assertEqual(
            high,
            "Disable",
            "Failed on get high low storage disabled.",
        )
        self.assertEqual(
            low,
            "Disable",
            "Failed on get high low storage disabled.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get high low storage disabled.",
        )

        (
            return_var,
            blob_disable,
            blob_size_disable,
        ) = self.gen.ghs_get_current_settings()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to get current settings.",
        )

        return_var = self.gen.ghs_set_current_settings(
            blob_enable, blob_size_enable
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed to set current settings.",
        )

        return_var, high, low = self.gen.ghs_get_high_low_rate_storage_enabled(
            "SyncChannels", "A"
        )
        self.assertEqual(
            high,
            "Enable",
            "Failed on set current settings.",
        )
        self.assertEqual(
            low,
            "Enable",
            "Failed on set current settings.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get high low storage enabled.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Manage mainframe settings API Functional Test Report",
            report_title="Manage mainframe settings API Functional Test Report",
        )
    )
