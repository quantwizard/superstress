#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2016
# Author: Liu Feng

import os
import re

def main():
    err_4200127 = 0
    err_4200125 = 0
    cards = 0
    total_res = 0
    re_4200127 = re.compile(r'4200127')
    re_4200125 = re.compile(r'4200125')
    path = os.path.join(os.path.dirname(__file__), r'ss.log')
    with open(path, 'r') as f:
        for line in f:
            if line.find(r'<res_data>') != -1:
                total_res += 1
                if line.find(r'CARD') != -1:
                    cards += 1
                elif re_4200125.search(line) is not None:
                    err_4200125 += 1
                elif re_4200127.search(line) is not None:
                    err_4200127 += 1

    print "The total response: %d" % total_res
    print "The cards: %d" % cards
    print "The error code 4200127: %d" % err_4200127
    print "The error code 4200125: %d" % err_4200125

if __name__ == '__main__':
    main()
