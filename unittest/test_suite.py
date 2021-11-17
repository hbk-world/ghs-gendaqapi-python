"""Gen Daq Python API unit test suite."""
import unittest
import sys

from HtmlTestRunner import HTMLTestRunner

import test_connection_handler
import test_json
import test_connection_api

sys.tracebacklimit = 0
# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_json))
suite.addTests(loader.loadTestsFromModule(test_connection_api))
suite.addTests(loader.loadTestsFromModule(test_connection_handler))

# initialize a runner, pass it your suite and run it
runner = HTMLTestRunner(
    combine_reports=True,
    open_in_browser=True,
    report_name="Python Driver Unittest Report",
    report_title="Python Driver Unittest Report",
)
runner.run(suite)
