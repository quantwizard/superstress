#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2016
# Author: Liu Feng

from ConfigParser import SafeConfigParser as scp
import ConfigParser
import os
import optparse
import re
import sys
# import pdb



class Stat(object):
    def __init__(self, app):
        # self.app = app
        parser = scp()
        dir_path = os.path.dirname(__file__)
        config_path = os.path.join(dir_path, r"statLog.ini")
        parser.read(config_path)
        self.opts = parser.options(app)
        self.search_dict = {}
        for opt in self.opts:
            self.search_dict[opt] = re.compile(parser.get(app, opt))

    def print_stat(self):
        # pdb.set_trace()
        results = {}
        total_res = 0
        for opt in self.search_dict:
            results[opt] = 0
        path = os.path.join(os.path.dirname(__file__), r'ss.log')
        with open(path, 'r') as f:
            for line in f:
                if line.find(r'<res_data>') != -1:
                    total_res += 1
                for opt, search_re in self.search_dict.iteritems():
                    if search_re.search(line) is not None:
                        results[opt] += 1
        print "The total response: %d" % total_res
        for option in results:
            print "The %s: %d" % (option, results[option])


def main():
    usage = '''Usage: %prog [-options][args]\r\n
    Make sure you have ss.log and configured statLog.ini.
    Example:
    1. %prog -a xmas       // print corresponding app statistics
    '''
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-a", "--app", dest="app_name", default="chun",
                      help="Specify the app for which you want to see the statistics [default: %default]")

    if len(sys.argv) == 1:
        parser.print_help()
        return

    options, args = parser.parse_args()
    stat = Stat(options.app_name)
    stat.print_stat()

if __name__ == '__main__':
    main()