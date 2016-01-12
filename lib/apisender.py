#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2016
# Author: Liu Feng

import httplib2
import base64
import json
from urlparse import urljoin
from logging import getLogger


lg = getLogger("sslogger")
# httplib2.debuglevel = 1


def sendAPI(http, email, password, host, path,
            head='', body='', count=1,
            msgType="GET"):
    if head == '' or head is None:
        headers = {
                    "Connection": "Keep-Alive",
                    "Cache-Control": "no-cache",
                }
        if email != '' and password != '':
            auth = base64.encodestring(email + ':' + password)
            headers["Authorization"] = "Basic " + auth.strip()
    else:
        headers = head

    url = urljoin(host, path)
    for i in range(count):
        lg.info(url)
        # lg.debug(body)
        response, data = http.request(url, msgType, headers=headers, body=body)
        # lg.debug(response)
        # lg.debug(data)
    return response, data

def parseResponse(response):
    if response['status'] == "200":
        return True
    else:
        return False

if __name__ == '__main__':
    http = httplib2.Http()
    url = "http://127.0.0.1:5000/"
    headers = {
                "Connection": "Keep-Alive",
                "Cache-Control": "no-cache",
                # "Content-Type": "application/json"
              }
    body = json.dumps({"openId":"eliutest"})
    res, data = sendAPI(http, '', '', url, '', headers, body, 1, 'POST')
    print data