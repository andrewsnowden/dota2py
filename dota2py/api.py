"""
Tools for accessing the Dota 2 match history web API
"""

import requests
import urllib

API_KEY = None
BASE_URL_PRODUCTION = "https://api.steampowered.com/IDOTA2Match_570/"
BASE_URL_TESTING = "https://api.steampowered.com/IDOTA2Match_205790/"


class RequestFailure(Exception):
    """
    Thrown when a request to the Dota 2 servers failed. Probably they are down.
    """
    def __init__(self, status_code, url):
        self.status_code = status_code
        self.url = url

    @classmethod
    def from_response(self, resp):
        self.status_code = resp.status_code
        self.url = resp.url

    def __str__(self):
        return 'Error accessing {}: Code {}'.format(self.url, self.status_code)


def set_api_key(key):
    """
    Set your API key for all further API queries
    """

    global API_KEY
    API_KEY = key


def url_map(base, params):
    """
    Return a URL with get parameters based on the params passed in

    @param params: HTTP GET parameters
    """

    url = base

    if len(params) == 0:
        #remove trailing ?&
        return url.rstrip("?&")

    if '?' not in url:
        url += "?"
    elif '?' in url:
        if not url.endswith("&") and not url.endswith("?"):
            url += "&"

    entries = []
    for key, value in params.iteritems():
        if value is not None:
            value = str(value)
            entries.append("%s=%s" % (urllib.quote_plus(key.encode("utf-8")),
                                      urllib.quote_plus(value.encode("utf-8"))))

    url += "&".join(entries)
    return str(url)

def get_page(url):
    """
    Fetch a page
    """

    import requests
    print 'GET %s' % (url, )
    resp = requests.get(url)
    if resp.status_code != requests.codes.ok:
        raise RequestFailure.from_response(resp)
    return resp


def make_request(name, params=None, version="V001", production_servers=True, key=None,
                 fetcher=get_page):
    """
    Make an API request
    """

    params = params or {}
    params["key"] = key or API_KEY

    if not params["key"]:
        raise ValueError("API key not set")

    base_url = BASE_URL_PRODUCTION if production_servers else BASE_URL_TESTING
    url = url_map("%s%s/%s/" % (base_url, name, version), params)
    return fetcher(url)


def get_match_history(start_at_match_id=None, player_name=None, hero_id=None,
                      skill=0, date_min=None, date_max=None, account_id=None,
                      league_id=None, matches_requested=None,
                      **kwargs):
    """
    List of most recent 25 matches before start_at_match_id
    """

    params = {
        "start_at_match_id": start_at_match_id,
        "player_name": player_name,
        "hero_id": hero_id,
        "skill": skill,
        "date_min": date_min,
        "date_max": date_max,
        "league_id": league_id,
        "matches_requested": matches_requested,
    }

    return make_request("GetMatchHistory", params, **kwargs)


def get_match_details(match_id, **kwargs):
    """
    Detailed information about a match
    """

    return make_request("GetMatchDetails", {"match_id": match_id}, **kwargs)

def get_prev_matches(n, start=None, date_max=None, **kwargs):
    """
    A generator yielding up to n matches one after another, starting with match
    start_id if given or the most recent match before date_max or now.
    """
    while n:
        resp = get_match_history(start_at_match_id=start, date_max=date_max, **kwargs)
        matches = resp.json['result']['matches']

        # We got the most (500) out of this query, move the date window to the past for the next query.
        if resp.json['result']['results_remaining'] == 0:
            date_max = matches[-1]['start_time']

        for match, _ in zip(matches, range(n)):
            yield match

        n -= len(matches)
        start = matches[-1]['match_id']-1

