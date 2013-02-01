import sys
from os.path import abspath, join, dirname
import os

# Some path fiddling to make sure we can access the module
sys.path.append(abspath(join(abspath(dirname(__file__)), "..")))

from dota2py import api

key = os.environ.get("DOTA2_API_KEY")
if not key:
    raise NameError("Please set the DOTA2_API_KEY environment variable")
api.set_api_key(key)

# Get all the most recent match played by the player 'acidfoo'
account_id = int(api.get_steam_id("acidfoo")["response"]["steamid"])

# Get a list of recent matches for the player
matches = api.get_match_history(account_id=account_id)["result"]["matches"]

# Get the full details for a match
match = api.get_match_details(matches[0]["match_id"])
print 'Match information:\n%s' % (match, )
