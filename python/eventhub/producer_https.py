#!/usr/bin/env python3

import os
import json
import requests
import datetime


def get_sas_token(namespace, event_hub, user, key):
    import urllib.parse
    import hmac
    import hashlib
    import base64
    import time

    if not (namespace or event_hub or user or key):
        return None
    uri = urllib.parse.quote_plus(
        "https://{}.servicebus.windows.net/{}".format(namespace, event_hub))
    sas = key.encode('utf-8')
    expiry = str(int(time.time() + 10000))
    string_to_sign = (uri + '\n' + expiry).encode('utf-8')
    signed_hmac_sha256 = hmac.HMAC(sas, string_to_sign, hashlib.sha256)
    signature = urllib.parse.quote(
        base64.b64encode(signed_hmac_sha256.digest()))
    return "SharedAccessSignature sr={}&sig={}&se={}&skn={}".format(uri, signature, expiry, user)


def get_http_header(namespace, event_hub, user, key):
    if not (namespace or event_hub or user or key):
        return None

    headers = {}
    headers['Content'] = "application/atom+xml;type=entry;charset=utf-8"
    headers['Authorization'] = get_sas_token(namespace, event_hub, user, key)
    headers['Host'] = "{}.servicebus.windows.net".format(namespace)
    return headers


def get_http_params():
    params = {}
    params['timeout'] = 60
    params['api-version'] = "2014-01"
    return params


namespace = os.environ["EVENT_HUBS_NAMESPACE"]
user = os.environ['EVENT_HUBS_POLICY']
key = os.environ['EVENT_HUBS_KEY']
event_hub = os.environ['EVENT_HUB_NAME']
headers = get_http_header(namespace, event_hub, user, key)
params = get_http_params()
data = {}
data['date'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
data['temp'] = "79.8"
uri = f"https://{namespace}.servicebus.windows.net/{event_hub}/messages"
r = requests.post(url=uri, headers=headers, params=params, data=json.dumps(data))
print(r)
