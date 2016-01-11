#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import httplib2
import base64
# import json
from urlparse import urljoin
from logging import getLogger
from threading import Lock
from . import logger
# import logger

lg = getLogger("sslogger")
# httplib2.debuglevel = 1

lock = Lock()
def sendAPI(http, email, password, host, path, head='', body='', count=1, msgType="GET"):    
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
    if lock.acquire(1):
        lg.info(url)
        lock.release()
    for i in range(count):
        response, data = http.request(url, msgType, headers=headers, body=body)
    return response, data

def parseResponse(response):
    if response['status'] == "200":
        return True
    else:
        return False
