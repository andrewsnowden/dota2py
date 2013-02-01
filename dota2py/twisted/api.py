from dota2py import api
from twisted.web import client
from twisted.python import util
from functools import partial
import json

set_api_key = api.set_api_key


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


get_steam_id = json_twisted_response(partial(api.get_steam_id.func,
    fetcher=client.getPage))

get_match_history = json_twisted_response(partial(api.get_match_history.func,
                                      fetcher=client.getPage))

get_match_details = json_twisted_response(partial(api.get_match_details.func,
                                      fetcher=client.getPage))

get_heroes = json_twisted_response(partial(api.get_heroes.func,
                                           fetcher=client.getPage))
