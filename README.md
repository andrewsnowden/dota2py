dota2py
=======

Python tools for Dota 2

Web API client
--------------

A thin wrapper around the Dota 2 web API described at:
[http://dev.dota2.com/showthread.php?t=47115](http://dev.dota2.com/showthread.php?t=47115)

This uses either the [requests](http://docs.python-requests.org/en/latest/index.html) library (dota2py/api.py), or [Twisted](http://www.twistedmatrix.com) (dota2py/twisted/api.py)

Replay Parser
-------------

This contains a Python port of [demoinfo2](https://developer.valvesoftware.com/wiki/Dota_2_Demo_Format), but will probably be expanded into more useful tools for Dota 2 replays
You will need [snappy](http://code.google.com/p/snappy/) and [Google Protocol Buffers](https://developers.google.com/protocol-buffers/) installed

To run the parser either run parser.py or in Linux use the dota2py_parser script

To show a summary of useful information from a replay, run summary.py or dota2py_summary (this functionality is a work in progress)

Running the tests
-----------------

There are a number of functional tests for the Web API. These require a valid Dota 2 API key, you can get one at:
[http://steamcommunity.com/dev/apikey](http://steamcommunity.com/dev/apikey)

To run the tests you must set the environment variable DOTA2_API_KEY to your key. In windows:

    set DOTA2_API_KEY=YOUR_KEY_HERE

and in linux:

    export DOTA2_API_KEY=YOUR_KEY_HERE

Once you have set your API key, the easiest way to run the tests is using nosetests (pip install nose).

To run all the tests:

    nosetests dota2py

To run a specific test:

    nosetests dota2py.funtests.test_api:ApiTest.test_get_steamid

To print out debug information you can add the following flags:

    -v -s --logging-config=debug_logging.cfg