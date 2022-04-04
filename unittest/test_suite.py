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

"""Gen Daq Python API unit test suite."""
import sys
import unittest

from HtmlTestRunner import HTMLTestRunner
from xmlrunner import XMLTestRunner

import test_acquisition_api
import test_channel_api
import test_connection_api
import test_connection_handler
import test_json
import test_mainframe_api
import test_manage_mainframe_settings
import test_manage_recordings
import test_recorder_api

if __name__ == "__main__":

    sys.tracebacklimit = 0
    # initialize the test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # add tests to the test suite
    suite.addTests(loader.loadTestsFromModule(test_json))
    suite.addTests(loader.loadTestsFromModule(test_connection_handler))
    suite.addTests(loader.loadTestsFromModule(test_connection_api))
    suite.addTests(loader.loadTestsFromModule(test_acquisition_api))
    suite.addTests(loader.loadTestsFromModule(test_mainframe_api))
    suite.addTests(loader.loadTestsFromModule(test_manage_recordings))
    suite.addTests(loader.loadTestsFromModule(test_manage_mainframe_settings))
    suite.addTests(loader.loadTestsFromModule(test_recorder_api))
    suite.addTests(loader.loadTestsFromModule(test_channel_api))

    # initialize a runner, pass it your suite and run it
    HTMLTestRunner(
        combine_reports=True,
        open_in_browser=False,
        report_name="Python Driver Unittest Report",
        report_title="Python Driver Unittest Report",
    ).run(suite)

    suite = unittest.TestSuite()

    # add tests to the test suite
    suite.addTests(loader.loadTestsFromModule(test_json))
    suite.addTests(loader.loadTestsFromModule(test_connection_handler))
    suite.addTests(loader.loadTestsFromModule(test_connection_api))
    suite.addTests(loader.loadTestsFromModule(test_acquisition_api))
    suite.addTests(loader.loadTestsFromModule(test_mainframe_api))
    suite.addTests(loader.loadTestsFromModule(test_manage_recordings))
    suite.addTests(loader.loadTestsFromModule(test_manage_mainframe_settings))
    suite.addTests(loader.loadTestsFromModule(test_recorder_api))
    suite.addTests(loader.loadTestsFromModule(test_channel_api))

    result = not XMLTestRunner(output="reports").run(suite).wasSuccessful()
    sys.exit(result)
