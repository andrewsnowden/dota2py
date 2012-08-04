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
