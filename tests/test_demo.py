"""Docstring"""
import unittest
import sys

import HtmlTestRunner


sys.tracebacklimit = 0
# can use mocking for connection to a mainframe


class TestDemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # run at start of test file
        pass

    @classmethod
    def tearDownClass(cls):
        # run at end of test file
        pass

    def setUp(self):
        # runs before each test
        pass

    def tearDown(self):
        # runs after each test
        pass

    def test_demo(self):
        pass


if __name__ == "__main__":
    # unittest.main()
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            open_in_browser=True,
            report_name="Demo Unittest Report",
            report_title="Demo Unittest Report",
        )
    )
