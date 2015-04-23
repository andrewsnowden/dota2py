"""
Tools for accessing the Dota 2 match history web API
"""

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

import logging
import json
from functools import wraps
import os

API_KEY = os.environ.get("DOTA2_API_KEY")
BASE_URL = "http://api.steampowered.com/IDOTA2Match_570/"
API_FUNCTIONS = {}

logger = logging.getLogger("dota2py")


def set_api_key(key):
    """
    Set your API key for all further API queries
    """

    global API_KEY
    API_KEY = key


def url_map(base, params):
    """
    Return a URL with get parameters based on the params passed in
    This is more forgiving than urllib.urlencode and will attempt to coerce
    non-string objects into strings and automatically UTF-8 encode strings.

    @param params: HTTP GET parameters
    """

    url = base

    if not params:
        url.rstrip("?&")
    elif '?' not in url:
        url += "?"

    entries = []
    for key, value in params.items():
         if value is not None:
            value = str(value)
            entries.append("%s=%s" % (quote_plus(key.encode("utf-8")),
                                      quote_plus(value.encode("utf-8"))))

    url += "&".join(entries)
    return str(url)


def get_page(url):
    """
    Fetch a page
    """

    import requests
    logger.debug('GET %s' % (url, ))
    return requests.get(url)


def make_request(name, params=None, version="V001", key=None, api_type="web",
                 fetcher=get_page, base=None, language="en_us"):
    """
    Make an API request
    """

    params = params or {}
    params["key"] = key or API_KEY
    params["language"] = language

    if not params["key"]:
        raise ValueError("API key not set, please set DOTA2_API_KEY")

    url = url_map("%s%s/%s/" % (base or BASE_URL, name, version), params)
    return fetcher(url)


def json_request_response(f):
    """
    Parse the JSON from an API response. We do this in a decorator so that our
    Twisted library can reuse the underlying functions
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        response.raise_for_status()
        return json.loads(response.content.decode('utf-8'))

    API_FUNCTIONS[f.__name__] = f
    return wrapper


@json_request_response
def get_match_history(start_at_match_id=None, player_name=None, hero_id=None,
                      skill=0, date_min=None, date_max=None, account_id=None,
                      league_id=None, matches_requested=None, game_mode=None,
                      min_players=None, tournament_games_only=None,
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
        "account_id": account_id,
        "league_id": league_id,
        "matches_requested": matches_requested,
        "game_mode": game_mode,
        "min_players": min_players,
        "tournament_games_only": tournament_games_only
    }

    return make_request("GetMatchHistory", params, **kwargs)


@json_request_response
def get_match_history_by_sequence_num(start_at_match_seq_num,
                                      matches_requested=None, **kwargs):
    """
    Most recent matches ordered by sequence number
    """
    params = {
        "start_at_match_seq_num": start_at_match_seq_num,
        "matches_requested": matches_requested
    }

    return make_request("GetMatchHistoryBySequenceNum", params,
        **kwargs)


@json_request_response
def get_match_details(match_id, **kwargs):
    """
    Detailed information about a match
    """
    return make_request("GetMatchDetails", {"match_id": match_id}, **kwargs)


@json_request_response
def get_steam_id(vanityurl, **kwargs):
    """
    Get a players steam id from their steam name/vanity url
    """
    params = {"vanityurl": vanityurl}
    return make_request("ResolveVanityURL", params, version="v0001",
        base="http://api.steampowered.com/ISteamUser/", **kwargs)


@json_request_response
def get_player_summaries(players, **kwargs):
    """
    Get players steam profile from their steam ids
    """
    if (isinstance(players, list)):
        params = {'steamids': ','.join(str(p) for p in players)}
    elif (isinstance(players, int)):
        params = {'steamids': players}
    else:
        raise ValueError("The players input needs to be a list or int")
    return make_request("GetPlayerSummaries", params, version="v0002",
        base="http://api.steampowered.com/ISteamUser/", **kwargs)


@json_request_response
def get_heroes(**kwargs):
    """
    Get a list of hero identifiers
    """
    return make_request("GetHeroes",
        base="http://api.steampowered.com/IEconDOTA2_570/", **kwargs)


def get_hero_image_url(hero_name, image_size="lg"):
    """
    Get a hero image based on name and image size
    """

    if hero_name.startswith("npc_dota_hero_"):
        hero_name = hero_name[len("npc_dota_hero_"):]

    valid_sizes = ['eg', 'sb', 'lg', 'full', 'vert']
    if image_size not in valid_sizes:
        raise ValueError("Not a valid hero image size")

    return "http://media.steampowered.com/apps/dota2/images/heroes/{}_{}.png".format(
        hero_name, image_size)


def get_item_image_url(item_name, image_size="lg"):
    """
    Get an item image based on name
    """

    return "http://media.steampowered.com/apps/dota2/images/items/{}_{}.png".format(
        item_name, image_size)


@json_request_response
def get_live_league_games(**kwargs):
    """
    Get a list of currently live league games
    """
    return make_request("GetLiveLeagueGames", **kwargs)


@json_request_response
def get_league_listing(**kwargs):
    """
    Get a list of leagues
    """
    return make_request("GetLeaguelisting", **kwargs)


@json_request_response
def get_scheduled_league_games(**kwargs):
    """
    Get a list of scheduled league games
    """
    return make_request("GetScheduledLeagueGames", **kwargs)
