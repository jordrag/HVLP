# encoding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

import sys
from test_suit import *
from inspect import isclass
import logging
import logging.config

sys.path.append(str("."))
sys.path.append(str(".."))

logging.config.fileConfig(b"..\\components\\test_logging.conf")


class Tester(object):
    """ Starts all "HVLP_NET" tests from test_suit. """

    def __init__(self):
        self.test_results = {}
        self.logger = logging.getLogger()
        self.cycle_time = 0.1

    def starter(self):
        """ Starts tests and logs results. """

        # Takes all classes for starting from test_suit
        classes = [x for x in dir(sys.modules[__name__])
                   if isclass(getattr(sys.modules[__name__], x))]
        for item in classes:
            if 'HVLP_NET' in item:
                self.test_results[item] = 0

        # Sorts tests and starts them in sorted order
        for test_name in sorted(self.test_results.keys()):
            cls = getattr(sys.modules[__name__], test_name)
            result = cls().execute()

            # Logs PASSED or FAILED in log file, depending on returned result
            if result:
                log_result = "PASSED"
            else:
                log_result = "FAILED"

            self.test_results[test_name] = result
            self.logger.info("Test: {0} - {1}".format(test_name, log_result))

            # Gives a break between tests
            sleep(self.cycle_time)


Tester().starter()
