from dota2py import api
from twisted.web import client
from twisted.python import util
from functools import partial
import json
import sys


def json_twisted_response(f):
    """
    Parse the JSON from an API response. We do this in a decorator so that our
    Twisted library can reuse the underlying functions
    """

    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        response.addCallback(lambda x: json.loads(x))
        return response

    wrapper.func = f
    wrapper = util.mergeFunctionMetadata(f.func, wrapper)
    return wrapper

set_api_key = api.set_api_key

# Set up copies of all of the API functions that use client.getPage
module = sys.modules.get(__name__)
if module:
    for name, func in api.API_FUNCTIONS.items():
        setattr(module, name, json_twisted_response(partial(func,
            fetcher=client.getPage)))
