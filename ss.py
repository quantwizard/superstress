#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2016
# Author: Liu Feng

import sys
import optparse
# import os
from lib.stresstest import StressTest

def Main():
    usage = '''Usage: %prog [-options][args]\r\n
    Example:
    1. %prog -a xmas -c 100         // stress test with xmas app, draw with 100 times
    2. %prog -a nine -p -c 200      // stress test with nine app, get H5 page with 200 times
    '''
    parser = optparse.OptionParser(usage=usage)
    # parser.add_option("-v", "--verbos",
    #                   action="store_true", dest="verbose", default=False,
    #                   help="Don't show the procession information [default: False]")

    parser.add_option("-a", "--app", dest="app_name", default="chun",
                      help="Specify the app you want to do stress test [default: %default]")

    parser.add_option("-c", "--count", dest="count", default="100",
                      help="Specify the http request times you want to sent [default: %default]")

    parser.add_option("-t", "--type", dest="test_type", default="draw",
                      help="Specify the test type. Currently only 2 types page/draw [default: %default]")

    if len(sys.argv) == 1:
        parser.print_help()
        return

    options, args = parser.parse_args()
    st = StressTest(options.app, options.test_type, options.count)
    st.stesstest()

if __name__ == '__main__':
    Main()