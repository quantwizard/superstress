#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2016
# Author: Liu Feng

import os
import re

def main():
    err_4110001 = 0
    err_4110003 = 0
    cards = 0
    total_res = 0
    re_4110001 = re.compile(r'4110001')
    re_4110003 = re.compile(r'4110003')
    path = os.path.join(os.path.dirname(__file__), r'ss.log')
    with open(path, 'r') as f:
        for line in f:
            if line.find(r'<res_data>') != -1:
                total_res += 1
                if line.find(r'cardid') != -1:
                    cards += 1
                elif re_4110003.search(line) is not None:
                    err_4110003 += 1
                elif re_4110001.search(line) is not None:
                    err_4110001 += 1

    print "The total response: %d" % total_res
    print "The cards: %d" % cards
    print "The error code 4110001: %d" % err_4110001
    print "The error code 4110003: %d" % err_4110003

if __name__ == '__main__':
    main()
