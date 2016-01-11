#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import httplib2
import base64
# import json
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
        response, data = http.request(url, msgType, headers=headers, body=body)
    return response, data

def parseResponse(response):
    if response['status'] == "200":
        return True
    else:
        return False
