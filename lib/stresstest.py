#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2016
# Author: Liu Feng

# from __future__ import division
from ConfigParser import SafeConfigParser as scp
import ConfigParser
from logging import getLogger
import httplib2
import json
import hashlib
import random
# import pdb
import threading
import os
from .apisender import *

lg = getLogger("sslogger")


class StressTest(object):

    def __init__(self, app, test_type, count, is_multiple=False):
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
            self.app = app
            self.is_multiple = is_multiple
            if self.app not in [
                    'nine', 'xmas', 'chun',
                    'rotate', 'lottery', 'scratch',
                    'box']:
                raise ParamError(self.app)
            self.test_type = test_type
            if self.test_type not in ['page', 'draw']:
                raise ParamError(self.test_type)
            self.count = int(count)

        except ConfigParser.Error, e:
            lg.error("StressTest init failed.")
            lg.error("Exception: %s" % e)
            raise e

    def __get_path(self):
        event_id = self.__get_eventid()
        if self.app == 'chun':
            if self.test_type == "draw":
                return "app/chun/views/%s/draw" % event_id
            elif self.test_type == "page":
                return "app/chun/views/" + event_id
            else:
                raise ParamError(self.test_type)
        elif self.app in ['nine', 'xmas', 'rotate', 'lottery', 'scratch', 'box']:
            if self.test_type == "draw":
                return "app/%s/mobile/%s/draw" % (self.app, event_id)
            elif self.test_type == "page":
                return "app/%s/mobile/%s" % (self.app, event_id)
            else:
                raise ParamError(self.test_type)
        else:
            raise ParamError(self.app)

    def __get_sessionid(self):
        if not self.email:
            raise ConfigError('email')
        if not self.password:
            raise ConfigError('password')

        path = "base/sessions"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache",
            "Content-Type": "application/json;charset=UTF-8",
        }
        account = {"email": self.email, "password": self.password}
        body = json.dumps(account)
        res, data = sendAPI(self.http, '', '', self.host, path, head=headers,
                            body=body, msgType="POST")
        userInfo = json.loads(data)
        lg.debug(userInfo)
        if userInfo and "sessionID" in userInfo:
            return userInfo["sessionID"]
        else:
            raise ConfigError('email or password')

    def __get_eventid(self):
        if self.app == "chun":
            path = "app/chun/lotteries?page=1&count=1"
        elif self.app in ['nine', 'xmas', 'rotate', 'lottery', 'scratch']:
            path = "app/%s/events?page=1&pageSize=1" % self.app
        elif self.app in ['box']:
            path = ("http://qing.mocha.server.sensoro.com/"
                    "app/%s/create?page=1&count=1" % self.app)
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache",
            "x-session-id": self.__get_sessionid()
        }
        res, data = sendAPI(self.http, '', '',
                            self.host, path,
                            head=headers, msgType="GET"
                            )
        lg.debug('res for getEventId: %s' % res)
        lg.debug('data for getEventId: %s' % data)
        if not parseResponse(res):
            lg.error("Get event id failed.")
            lg.error("res: %s" % res)
            lg.error("data: %s" % data)
            raise GetEventError(data)
        eventInfo = json.loads(data)
        if self.app in ['chun', 'box']:
            return eventInfo["data"][0]["_id"]
        return eventInfo["events"][0]["_id"]

    def __get_random_openid(self):
        random_number = random.randint(1, 1000)
        now = time.strftime("%Y-%m-%d %X", time.localtime())
        return hashlib.md5(now+str(random_number)).hexdigest()

    def __sendAPI(self, http, path, headers, body, count, msg_type):
        if self.is_multiple:
            openid = self.__get_random_openid()
            cookie = ("snsapi_userinfo:%s="
                      '{"openid":"%s"}') % (self.appid, openid)
            headers = {
                        "Connection": "Keep-Alive",
                        "Cache-Control": "no-cache",
                        "Content-Type": "application/json",
                        "Cookie": cookie,
                     }
            if self.app in ['box']:
                body = json.dumps({"openId": openid})

        url = urljoin(self.host, path)
        for i in xrange(count):
            lg.info(url)
            # lg.debug(body)
            response, data = http.request(url, msg_type, headers=headers, body=body)
            # lg.debug(response)
            # lg.debug(data)

    def stress_test(self):
        path = self.__get_path()
        if self.app in ['box']:
            # pdb.set_trace()
            body = json.dumps({"openId": self.openid})
        else:
            body = ""
        if self.app in ['chun', 'box']:
            msg_type = "POST"
        else:
            msg_type = "GET"
        t_count = 10
        threads = []
        if not self.is_multiple:
            cookie = ("snsapi_userinfo:%s="
                      '{"openid":"%s"}') % (self.appid, self.openid)
            head = {
                "Connection": "Keep-Alive",
                "Cache-Control": "no-cache",
                "Content-Type": "application/json",
                "Cookie": cookie,
            }
            for i in range(t_count):
                # http object is not thread safe, so we have to
                # create http object for each thread
                http = httplib2.Http()
                t = threading.Thread(
                    target=self.__sendAPI,
                    args=(http, path, head, body,
                          self.count/t_count, msg_type)
                )
                threads.append(t)
                t.setDaemon(True)
                t.start()
        else:
            for i in range(t_count):
                # http object is not thread safe, so we have to
                # create http object for each thread
                http = httplib2.Http()
                t = threading.Thread(
                    target=self.__sendAPI,
                    args=(http, path, '', '',
                          self.count/t_count, msg_type)
                )
                threads.append(t)
                t.setDaemon(True)
                t.start()
        for t in threads:
            t.join(10000)


class ParamError(Exception):
    def __init__(self, wrong_param):
        super(ParamError, self).__init__()
        self.value = wrong_param


class GetEventError(Exception):
    def __init__(self, res_data):
        super(GetEventError, self).__init__()
        self.value = res_data


class ConfigError(Exception):
    def __init__(self, config_param):
        super(GetEventError, self).__init__()
        self.value = config_param
