"""
Functional tests for the web API
"""

import unittest
import os

from dota2py import api, data

STEAM_NAME = "acidfoo"
STEAM_ID = 76561198042433230
MATCH_ID = 113514700
MATCH_SEQ_NUM = 104373116


class ApiTest(unittest.TestCase):
    def setUp(self):
        key = os.environ.get("DOTA2_API_KEY")
        if not key:
            raise NameError("Please set the DOTA2_API_KEY environment variable")
        api.set_api_key(key)

    def test_get_steam_id(self):
        """
        Get a steam ID from a steam account name
        """
        j = api.get_steam_id("acidfoo")
        self.assertEquals(j["response"]["success"], 1)
        self.assertEquals(j["response"]["steamid"], str(STEAM_ID))

    def test_match_history(self):
        """
        Get a list of the latest matches
        """
        j = api.get_match_history()
        self.assertEquals(j["result"]["status"], 1)
        self.assertIn("matches", j["result"])

    def test_player_match_history(self):
        """
        Get the latest matches for a particular player
        """
        j = api.get_match_history(account_id=STEAM_ID)
        self.assertEquals(j["result"]["status"], 1)
        self.assertTrue("matches" in j["result"])

        matches = j["result"]["matches"]

        # Check that this player is in each of the games
        steam_id_32 = data.get_steam_id_32(STEAM_ID)

        for match in matches:
            contained_player = False
            for player in match["players"]:
                if player["account_id"] == steam_id_32:
                    contained_player = True
                    break

            self.assertTrue(contained_player)

    def test_get_match_details(self):
        """
        Get the full details from a match
        """
        j = api.get_match_details(MATCH_ID)
        self.assertIn("result", j)
        self.assertEquals(j["result"]["match_id"], MATCH_ID)
        self.assertIn("players", j["result"])

    def test_get_match_history_by_sequence_num(self):
        """
        Get matches after a specific sequence number
        """
        j = api.get_match_history_by_sequence_num(MATCH_SEQ_NUM, 10)

        self.assertEquals(j["result"]["status"], 1)
        self.assertIn("matches", j["result"])

    def test_get_heroes(self):
        """
        Get list of hero identifiers
        """
        j = api.get_heroes()
        self.assertIn("result", j)
        heroes = j["result"]["heroes"]
        hero = heroes[0]
        self.assertIn("localized_name", hero)
        self.assertIn("name", hero)
        self.assertIn("id", hero)

    def test_get_live_league_games(self):
        """
        Get list of currently live league games
        """
        j = api.get_live_league_games()
        self.assertIn("result", j)
        self.assertIn("games", j["result"])

    def test_get_league_listing(self):
        """
        Get list of leagues
        """
        j = api.get_league_listing()
        self.assertIn("result", j)
        self.assertIn("leagues", j["result"])
