import sys
from os.path import abspath, join, dirname
import os

# Some path fiddling to make sure we can access the module
sys.path.append(abspath(join(abspath(dirname(__file__)), "..")))

from dota2py.twisted import api
from twisted.internet import reactor, defer
from twisted.python import log

key = os.environ.get("DOTA2_API_KEY")
if not key:
    raise NameError("Please set the DOTA2_API_KEY environment variable")
api.set_api_key(key)


@defer.inlineCallbacks
def run():
    result = yield api.get_steam_id("acidfoo")
    account_id = int(result["response"]["steamid"])

    result = yield api.get_match_history(account_id=account_id)
    matches = result["result"]["matches"]

    result = yield api.get_match_details(matches[0]["match_id"])
    print 'Match information:\n%s' % (result, )

    reactor.stop()


log.startLogging(sys.stdout)
reactor.callWhenRunning(run)
reactor.run()
