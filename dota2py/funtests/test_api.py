"""
Functional tests for the web API
"""

import unittest
import os
import json

from dota2py import api, data

STEAM_NAME = "acidfoo"
STEAM_ID = 76561198042433230


class ApiTest(unittest.TestCase):
    def setUp(self):
        key = os.environ.get("DOTA2_API_KEY")
        if not key:
            raise NameError("Please set the DOTA2_API_KEY environment variable")
        api.set_api_key(key)

    def test_get_steamid(self):
        """
        Test fetching a steam ID from a steam account name
        """
        response = api.get_steamid("acidfoo")
        self.assertEquals(response.status_code, 200)

        j = json.loads(response.content)

        self.assertEquals(j["response"]["success"], 1)
        self.assertEquals(j["response"]["steamid"], STEAM_ID)

    def test_match_history(self):
        """
        Test fetching the latest matches
        """

        response = api.get_match_history()
        self.assertEquals(response.status_code, 200)

        j = json.loads(response.content)

        self.assertEquals(j["result"]["status"], 1)
        self.assertIn("matches", j["result"])

    def test_player_match_history(self):
        """
        Test fetching a players match history
        """
        response = api.get_match_history(account_id=STEAM_ID)
        self.assertEquals(response.status_code, 200)

        j = json.loads(response.content)
        self.assertEquals(j["result"]["status"], 1)
        self.assertTrue("matches" in j["result"])

        matches = j["result"]["matches"]

        # Check that this player is in each of the games
        steamid_32 = data.get_steamid_32(STEAM_ID)

        for match in matches:
            contained_player = False
            for player in match["players"]:
                if player["account_id"] == steamid_32:
                    contained_player = True
                    break

            self.assertTrue(contained_player)
