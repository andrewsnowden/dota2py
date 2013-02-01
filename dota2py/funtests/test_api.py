"""
Functional tests for the web API
"""

from unittest import TestCase
import os
import json

from dota2py import api


class ApiTest(TestCase):
    def setUp(self):
        key = os.environ.get("DOTA2_API_KEY")
        if not key:
            raise NameError("Please set the DOTA2_API_KEY environment variable")
        api.set_api_key(key)

    def test_get_steamid(self):
        response = api.get_steamid("acidfoo")
        self.assertEquals(response.status_code, 200)

        j = json.loads(response.content)

        self.assertEquals(j["response"]["success"], 1)
        self.assertEquals(j["response"]["steamid"], u'76561198042433230')
