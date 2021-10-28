import unittest
import sys

from HtmlTestRunner import HTMLTestRunner

import test_connections
import test_demo

sys.tracebacklimit = 0
# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_demo))
suite.addTests(loader.loadTestsFromModule(test_connections))

# initialize a runner, pass it your suite and run it
# runner = unittest.TextTestRunner(verbosity=3)
# result = runner.run(suite)
runner = HTMLTestRunner(
    combine_reports=True,
    open_in_browser=True,
    report_name="Python Driver Unittest Report",
    report_title="Python Driver Unittest Report",
)
runner.run(suite)
