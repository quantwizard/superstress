#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import os


logger = logging.getLogger("autologger")
logger.setLevel(logging.DEBUG)
logPath = os.path.join(os.path.dirname(__file__), r"../ss.log")
handler = logging.FileHandler(logPath)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s: %(filename)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
