from dota2py import api
from twisted.web import client
import functools

get_match_history = functools.partial(api.get_match_history,
                                      fetcher=client.getPage)

get_match_details = functools.partial(api.get_match_details,
                                      fetcher=client.getPage)
