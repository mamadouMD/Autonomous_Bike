#!/usr/bin/env python3

import requests
import geopy

class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)

currcoord = geopy.point.Point(38.99262,-76.9373,0)

jsonpost = {
    'longitude': currcoord.longitude,
    'latitude': currcoord.latitude,
    'deviceID': 123456
    }
resp = requests.post('https://us-central1-fleet-8b5a9.cloudfunctions.net/sendPulse', json=jsonpost)
print(resp)
print(resp.status_code)

if resp.status_code != 201 and resp.status_code != 200:
    raise ApiError('Post was not successful: {}'.format(resp.status_code))
print('Sent GPS coordinate')
