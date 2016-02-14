#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2016
# Author: Liu Feng

import sys
import optparse
# import os
from lib.stresstest import *
from lib.logger import config_logger


def Main():
    usage = '''Usage: %prog [-options][args]. If -c and/or -u is not specified, use default value.\r\n
    Example:
    1. %prog -a xmas -c 10 -u 100       // stress test with xmas app, draw with 100 users and each user draw 10 times
    2. %prog -a nine -t page -v         // stress test with nine app, get H5 page of the app. 
    '''
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-a", "--app", dest="app_name", default="chun",
                      help="Specify the app you want to do stress test [default: %default]")
    parser.add_option("-c", "--count", dest="count", default="1",
                      help="Specify the http request times for each user [default: %default]")
    parser.add_option("-u", "--users", dest="users", default="100",
                      help="Specify how many different users [default: %default]")
    parser.add_option("-t", "--type", dest="test_type", default="draw",
                      help="Specify the test type. Currently only 2 types page/draw [default: %default]")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Enable console output.")
    parser.add_option("-r", "--response",
                      action="store_true", dest="response", default=False,
                      help="Enable http response/data output.")

    if len(sys.argv) == 1:
        parser.print_help()
        return

    options, args = parser.parse_args()
    config_logger(options.verbose)
    try:
        st = StressTest(
            options.app_name, options.test_type,
            options.count, options.users, options.vverbose)
        st.stress_test()
    except ParamError, e:
        print "The parameter you input is wrong: %s" % e.value
    except GetEventError, e:
        print "Get event id failed."
        print "The response info is: %s" % e.value
    except ConfigError, e:
        print "Your config [%s] in mainConfig.ini may be wrong." % e.value

if __name__ == '__main__':
    Main()
