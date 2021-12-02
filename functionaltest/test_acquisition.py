"""Acquisition Control API functional test."""

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


class TestAcquisition(unittest.TestCase):
    """Acquisition Control API functional test."""

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

    def test_preview(self):
        """Test Preview."""

        return_var = self.gen.ghs_start_preview()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to start a preview mode.",
        )

        return_var = self.gen.ghs_stop_preview()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to stop preview mode.",
        )

    def test_preview_not_idle(self):
        """Test start preview when system not idle."""

        self.gen.ghs_start_preview()

        return_var = self.gen.ghs_start_preview()
        self.assertEqual(
            return_var,
            "SystemNotIdle",
            "Failed on preview when system not idle.",
        )

    def test_not_in_preview(self):
        """Test when not in preview mode."""

        return_var = self.gen.ghs_stop_preview()
        self.assertEqual(
            return_var,
            "SystemNotInPreview",
            "Failed when not in preview mode.",
        )

    def test_recording(self):
        """Test recording."""

        return_var = self.gen.ghs_start_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to start a recording.",
        )

        return_var = self.gen.ghs_pause_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to pause a recording.",
        )

        time.sleep(1)

        return_var = self.gen.ghs_resume_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to resume a recording.",
        )

        return_var = self.gen.ghs_stop_recording()
        self.assertEqual(
            return_var,
            "OK",
            "Failed to stop recording.",
        )

    def test_recording_not_idle(self):
        """Test start recording when system not idle."""

        self.gen.ghs_start_recording()

        return_var = self.gen.ghs_start_recording()
        self.assertEqual(
            return_var,
            "SystemNotIdle",
            "Failed on recording when system not idle.",
        )

    def test_double_pause(self):
        """Test pause recording when already paused."""

        self.gen.ghs_start_recording()
        self.gen.ghs_pause_recording()
        time.sleep(1)

        return_var = self.gen.ghs_pause_recording()
        self.assertEqual(
            return_var,
            "SystemNotRecording",
            "Failed on trying double pause.",
        )

    def test_double_resume(self):
        """Test resume recording when already resumed."""

        self.gen.ghs_start_recording()
        self.gen.ghs_pause_recording()
        time.sleep(1)
        self.gen.ghs_resume_recording()

        return_var = self.gen.ghs_resume_recording()
        self.assertEqual(
            return_var,
            "SystemNotPaused",
            "Failed on trying double resume.",
        )

    def test_not_recording(self):
        """Test when not recording."""

        return_var = self.gen.ghs_stop_recording()
        self.assertEqual(
            return_var,
            "SystemNotRecording",
            "Failed when not recording.",
        )

    def test_not_paused(self):
        """Test when recording not paused."""

        return_var = self.gen.ghs_resume_recording()
        self.assertEqual(
            return_var,
            "SystemNotPaused",
            "Failed when recording not paused.",
        )

    # to check
    def test_preview_recording(self):
        """Test to start recording when in preview."""

        self.gen.ghs_start_preview()

        return_var = self.gen.ghs_start_recording()
        self.assertEqual(
            return_var,
            "SystemNotIdle",
            "Failed on start recording when in preview.",
        )

    def test_recording_preview(self):
        """Test to start recording when in preview."""

        self.gen.ghs_start_recording()

        return_var = self.gen.ghs_start_preview()
        self.assertEqual(
            return_var,
            "SystemNotIdle",
            "Failed on start recording when in preview.",
        )

    def test_get_state_idle(self):
        """Test get state when state idle."""

        return_var = self.gen.ghs_get_acquisition_state()
        self.assertEqual(
            return_var,
            ("OK", "Idle"),
            "Failed get state in idle.",
        )

    def test_get_state_preview(self):
        """Test get state when in preview."""

        self.gen.ghs_start_preview()

        return_var = self.gen.ghs_get_acquisition_state()
        self.assertEqual(
            return_var,
            ("OK", "Preview"),
            "Failed get state in preview.",
        )

    def test_get_state_recording(self):
        """Test get state when in recording."""

        self.gen.ghs_start_recording()

        return_var = self.gen.ghs_get_acquisition_state()
        self.assertEqual(
            return_var,
            ("OK", "Recording"),
            "Failed get state in recording.",
        )

    def test_get_state_paused(self):
        """Test get state when in recording paused."""

        self.gen.ghs_start_recording()
        self.gen.ghs_pause_recording()

        return_var = self.gen.ghs_get_acquisition_state()
        self.assertEqual(
            return_var,
            ("OK", "Pause"),
            "Failed get state in recording paused.",
        )

    def test_get_time_not_rec(self):
        """Test get time when system not recording."""

        return_var = self.gen.ghs_get_acquisition_time()
        self.assertEqual(
            return_var,
            ("SystemNotRecording", None),
            "Failed get time when system not recording.",
        )

    def test_get_time_preview(self):
        """Test get time when in preview."""

        self.gen.ghs_start_preview()
        time.sleep(1)
        return_var = self.gen.ghs_get_acquisition_time()
        self.assertEqual(
            isinstance(return_var[1], float),
            True,
            "Failed get time when in preview.",
        )

    def test_get_time_recording(self):
        """Test get time when recording."""

        self.gen.ghs_start_recording()
        time.sleep(1)
        return_var = self.gen.ghs_get_acquisition_time()
        self.assertEqual(
            isinstance(return_var[1], float),
            True,
            "Failed get time when recording.",
        )

    def test_get_time_pause(self):
        """Test get time when recording pause."""

        self.gen.ghs_start_recording()
        time.sleep(1)
        time_1 = self.gen.ghs_get_acquisition_time()[1]
        self.gen.ghs_pause_recording()
        time.sleep(2)
        time_2 = self.gen.ghs_get_acquisition_time()[1]
        self.assertEqual(
            time_1 == time_2,
            False,
            "Failed get time when recording pause.",
        )

    # to check
    def test_get_start_time_not_rec(self):
        """Test get start time when system not recording."""

        return_var = self.gen.ghs_get_acquisition_start_time()
        self.assertEqual(
            return_var,
            ("SystemNotRecording", None, None, None),
            "Failed get start time when system not recording.",
        )

    def test_get_start_time_preview(self):
        """Test get start time in preview."""

        self.gen.ghs_start_preview()
        time.sleep(1)
        return_var = self.gen.ghs_get_acquisition_start_time()
        result_type = (
            isinstance(return_var[1], int)
            and isinstance(return_var[2], int)
            and isinstance(return_var[3], float)
        )
        self.assertEqual(
            result_type,
            True,
            "Failed get start time in preview.",
        )

    def test_get_start_time_recording(self):
        """Test get start time when recording."""

        self.gen.ghs_start_recording()
        time.sleep(1)
        return_var = self.gen.ghs_get_acquisition_start_time()
        result_type = (
            isinstance(return_var[1], int)
            and isinstance(return_var[2], int)
            and isinstance(return_var[3], float)
        )
        self.assertEqual(
            result_type,
            True,
            "Failed get start time when recording.",
        )

    def test_get_start_time_pause(self):
        """Test get start time when recording paused."""

        self.gen.ghs_start_recording()
        time.sleep(1)
        time_1 = self.gen.ghs_get_acquisition_start_time()[1:]
        self.gen.ghs_pause_recording()
        self.gen.ghs_resume_recording()
        time.sleep(1)
        time.sleep(2)
        time_2 = self.gen.ghs_get_acquisition_start_time()[1:]

        self.assertEqual(
            time_1 == time_2,
            True,
            "Failed get start time when recording paused.",
        )

    # to check
    def test_trigger(self):
        """Test trigger when not recording or in preview."""

        return_var = self.gen.ghs_trigger()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on trigger when not recording or in preview.",
        )

    # to check
    def test_trigger_preview(self):
        """Test trigger when in preview."""

        self.gen.ghs_start_preview()
        time.sleep(1)

        return_var = self.gen.ghs_trigger()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on trigger when in preview.",
        )

    def test_trigger_recording(self):
        """Test trigger when recording."""

        self.gen.ghs_start_recording()
        time.sleep(1)

        return_var = self.gen.ghs_trigger()
        self.assertEqual(
            return_var,
            "OK",
            "Failed on trigger when recording.",
        )


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Acquisition Control API Functional Test Report",
            report_title="Acquisition Control API Functional Test Report",
        )
    )
