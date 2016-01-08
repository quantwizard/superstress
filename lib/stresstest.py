#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2016
# Author: Liu Feng

from ConfigParser import SafeConfigParser as scp
from logging import getLogger
import httplib2
import threading
import os
from . import logger
from .apisender import sendAPI

lg = getLogger("autologger")


class StressTest(object):

    def __init__(self, app, type, count):
        try:
            parser = scp()
            dir_path = os.path.dirname(__file__)
            config_path = os.path.join(dir_path,
                                       r"../mainConfig.ini")
            parser.read(config_path)
            self.http = httplib2.Http()
            self.host = parser.get('hostinfo', 'host')
            self.email = parser.get('userinfo', 'email')
            self.password = parser.get('userinfo', 'password')
            self.customerid = parser.get('userinfo', 'customerid')
            self.openid = parser.get('userinfo', 'openid')
            self.appid = parser.get('appinfo', 'appid')

        except Exception, e:
            lg.error("StressTest init failed.")
            lg.error("Exception: %s" % e)

    def get_path(self):
        pass

    def stress_test(self):
        path = self.get_path()
        if self.app == "chun":
            msgType = "POST"
        else:
            msgType = "GET"

        cookie = ("snsapi_userinfo:%s="
                  "{'openid':'%s'}") % (self.appid, self.openid)
        head = {
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache",
            "Cookie": cookie,
        }
        threads = []
        for i in range(20):
            t = threading.Thread(
                target=sendAPI,
                args=(self.http, '', '', self.host,
                      path, head, '',
                      self.count, msgType)
            )
            threads.append(t)
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join(10000)
