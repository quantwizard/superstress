#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import os


logger = logging.getLogger("autologger")
logger.setLevel(logging.DEBUG)
logPath = "/Users/eliu/git/API_Auto/API_Auto.log"
handler = logging.FileHandler(logPath)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s: %(filename)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == '__main__':
    logger.debug(
    "this is debug info\
    second line?")