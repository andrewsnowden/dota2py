dota2py
=======

Python tools for Dota 2

Web API client
--------------

A thin wrapper around the Dota 2 WebAPI described ([http://dev.dota2.com/showthread.php?t=47115](http://dev.dota2.com/showthread.php?t=47115))

This uses either the [requests](http://docs.python-requests.org/en/latest/index.html) library ([dota2py/api.py](dota2py/api.py)), or [Twisted](http://www.twistedmatrix.com) ([dota2py/twisted/api.py](dota2py/twisted/api.py))

To use the Web API you must have a valid steam API key. You can get one at [http://steamcommunity.com/dev/apikey](http://steamcommunity.com/dev/apikey)

More information about the API can be found in [this thread](http://dev.dota2.com/showthread.php?t=58317) and in [the WebAPI dev forums](http://dev.dota2.com/forumdisplay.php?f=411)

### WebAPI examples:

Examples code for both the standard and Twisted APIs can be found in the [examples folder](dota2py/examples).

#### Find the latest match for a player

```python
# Get all the most recent match played by the player 'acidfoo'
account_id = int(api.get_steam_id("acidfoo")["response"]["steamid"])

# Get a list of recent matches for the player
matches = api.get_match_history(account_id=account_id)["result"]["matches"]

# Get the full details for a match
match = api.get_match_details(matches[0]["match_id"])
```

Replay Parser
-------------

This contains a Python port of [demoinfo2](https://developer.valvesoftware.com/wiki/Dota_2_Demo_Format), but will probably be expanded into more useful tools for Dota 2 replays
You will need [snappy](http://code.google.com/p/snappy/) and [Google Protocol Buffers](https://developers.google.com/protocol-buffers/) installed

To run the parser either run parser.py or in Linux use the dota2py_parser script

To show a summary of useful information from a replay, run summary.py or dota2py_summary (this functionality is a work in progress)

Installation
------------

Install via pip:

    $ pip install dota2py

or, install via easy_install:

    $ easy_install dota2py

Running the tests
-----------------

There are a number of functional tests for the Web API. To run the tests you must set the environment variable DOTA2_API_KEY to your key. In windows:

    > set DOTA2_API_KEY=YOUR_KEY_HERE

and in linux:

    $ export DOTA2_API_KEY=YOUR_KEY_HERE

Once you have set your API key, the easiest way to run the tests is using nosetests (pip install nose).

To run all the tests:

    nosetests dota2py

To run a specific test:

    nosetests dota2py.funtests.test_api:ApiTest.test_get_steam_id

To print out debug information you can add the following flags:

    -v -s --logging-config=debug_logging.cfg