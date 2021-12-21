"""Manage recordings API functional test."""

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


class TestManageRecordings(unittest.TestCase):
    """Manage recordings API functional test."""

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

    def test_set_get_storage_location(self):
        """Test to set then get storage location to see if change gets
        reflected.
        """

        return_var = self.gen.ghs_set_storage_location("Local1")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set storage location.",
        )

        return_var, storage_location = self.gen.ghs_get_storage_location()
        self.assertEqual(
            storage_location,
            "Local1",
            "Failed on get storage location.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get storage location.",
        )

    def test_wrong_set_get_storage_location(self):
        """Test to set remote location then get previous storage
        location.
        """

        return_var = self.gen.ghs_set_storage_location("Local1")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set correct storage location.",
        )

        return_var = self.gen.ghs_set_storage_location("Remote")
        self.assertEqual(
            return_var,
            "IncompatibleStorage",
            "Failed on set incorrect storage location.",
        )

        return_var, storage_location = self.gen.ghs_get_storage_location()
        self.assertEqual(
            storage_location,
            "Local1",
            "Failed on get storage location.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get storage location.",
        )

    def test_set_get_recording_name(self):
        """Test to set then get recording name to see if change gets
        reflected.
        """

        return_var = self.gen.ghs_set_storage_location("Local1")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set mainframe as storage location.",
        )

        return_var = self.gen.ghs_set_recording_name("Test1", 2)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set recording name.",
        )

        (
            return_var,
            recording_name,
            recording_index,
        ) = self.gen.ghs_get_recording_name()
        self.assertEqual(
            recording_name,
            "Test1",
            "Failed on get recording name.",
        )
        self.assertEqual(
            recording_index,
            2,
            "Failed on get recording name.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get recording name.",
        )

    def test_wrong_set_get_recording_name(self):
        """Test to set wrong recording name then get previous set
        recording name to see if change persist reflected.
        """

        return_var = self.gen.ghs_set_recording_name("Test1", 2)
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set correct recording name.",
        )

        return_var = self.gen.ghs_set_recording_name("Test1", "1")
        self.assertEqual(
            return_var,
            "InvalidDataType",
            "Failed on set wrong recording name.",
        )

        (
            return_var,
            recording_name,
            recording_index,
        ) = self.gen.ghs_get_recording_name()
        self.assertEqual(
            recording_name,
            "Test1",
            "Failed on get recording name.",
        )
        self.assertEqual(
            recording_index,
            2,
            "Failed on get recording name.",
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on get recording name.",
        )

    def test_delete_last_recording(self):
        """Test delete last recording."""

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
            "Failed on start recording.",
        )

        return_var = self.gen.ghs_stop_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on stop recording.",
        )

        time.sleep(2)

        return_var = self.gen.ghs_delete_last_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on delete last recording.",
        )

    def test_no_recording_delete_last_recording(self):
        """Test delete last recording when no recording."""

        return_var = self.gen.ghs_set_storage_location("Local1")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set mainframe as storage location.",
        )

        return_var = self.gen.ghs_delete_all_recordings()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to delete all recording.",
        )

        return_var = self.gen.ghs_delete_last_recording()
        self.assertEqual(
            return_var,
            "RecordingNotFound",
            "Failed on delete last recording when no recording.",
        )

    def test_delete_all_recording(self):
        """Test delete all recording."""

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
            "Failed on start recording.",
        )

        return_var = self.gen.ghs_stop_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on stop recording.",
        )

        time.sleep(2)

        return_var = self.gen.ghs_start_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on start recording.",
        )

        return_var = self.gen.ghs_stop_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on stop recording.",
        )

        time.sleep(2)

        return_var = self.gen.ghs_delete_all_recordings()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on delete all recording.",
        )

    def test_set_get_high_low_srorage_enabled(self):
        """Test to set then get high low storage enabled."""

        return_var = self.gen.ghs_set_storage_location("Local1")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set mainframe as storage location.",
        )

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

    def test_wrong_set_get_high_low_srorage_enabled(self):
        """Test to set wrong high low storage enabled then get previous
        set values
        """

        return_var = self.gen.ghs_set_storage_location("Local1")
        self.assertEqual(
            return_var,
            "OK",
            "Failed on set mainframe as storage location.",
        )

        return_var = self.gen.ghs_set_high_low_rate_storage_enabled(
            "SyncChannels", "A", "Enable", "Enable"
        )
        self.assertEqual(
            return_var,
            "OK",
            "Failed on correct set high low storage enabled.",
        )

        return_var = self.gen.ghs_set_high_low_rate_storage_enabled(
            "SyncChannels", "A", "Abled", "Enable"
        )
        self.assertEqual(
            return_var,
            "InvalidDataType",
            "Failed on incorrect set high low storage enabled.",
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


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Manage recordings API Functional Test Report",
            report_title="Manage recordings API Functional Test Report",
        )
    )
