# -*- coding: utf-8 -*-
import requests


class PantheonClient(object):
    def __init__(self):
        self.url = 'http://api.mjtop.net'

    def _request(self, method, params):
        resp = requests.post(
            self.url,
            json={
                "jsonrpc": '2.0',
                "id": 1,
                "method": method,
                "params": params,
            }
        ).json()
        return resp['result']

    def get_last_games(self, event_id):
        return self._request('getLastGames', {"eventId": event_id, "limit": 10000, "offset": 0})

