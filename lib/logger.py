#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2016
# Author: Liu Feng

import logging
import os
import time

def config_logger(is_verbose=False):
    logger = logging.getLogger("sslogger")
    logger.setLevel(logging.DEBUG)
    logPath = os.path.join(os.path.dirname(__file__), r"../ss.log")
    if os.path.exists(logPath):
        newname = logPath + time.ctime(os.path.getctime(logPath)).replace(' ', '_')
        os.rename(logPath, newname)
    file_handler = logging.FileHandler(logPath)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(filename)s: %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if is_verbose:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
