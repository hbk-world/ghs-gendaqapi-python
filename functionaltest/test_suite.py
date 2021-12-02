"""Gen Daq Python API functional test suite."""
import sys
import unittest

from HtmlTestRunner import HTMLTestRunner

sys.tracebacklimit = 0
# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite

# initialize a runner, pass it your suite and run it
runner = HTMLTestRunner(
    combine_reports=True,
    open_in_browser=True,
    report_name="Python Driver Functional Test Report",
    report_title="Python Driver Functional Test Report",
)
runner.run(suite)
