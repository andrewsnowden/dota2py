"""
ID lookups from data files

Thanks to Lazze for the item list:
http://dev.dota2.com/showthread.php?t=47115&page=16&p=296787#post296787
"""

import os.path
import json

HEROES_CACHE = {}
ITEMS_CACHE = {}

GAME_MODES = {
    "dota_game_mode_0": "-",
    "dota_game_mode_1": "All Pick",
    "dota_game_mode_2": "Captains Mode",
    "dota_game_mode_3": "Random Draft",
    "dota_game_mode_4": "Single Draft",
    "dota_game_mode_5": "All Random",
    "dota_game_mode_6": "-",
    "dota_game_mode_7": "Diretide",
    "dota_game_mode_8": "Reverse Captains Mode",
    "dota_game_mode_9": "The Greeviling",
    "dota_game_mode_10": "Tutorial",
    "dota_game_mode_11": "Mid Only",
    "dota_game_mode_12": "Least Played",
    "dota_game_mode_13": "New Player Pool",
    "dota_game_mode_14": "Compendium",
    "dota_game_mode_15": "Wraith Night",
    "dota_game_mode_16": "Captains Draft",
    "dota_game_mode_17": "Auto Draft"
}

REPLAY_GAME_MODE = {
    1: "All Pick",
    2: "Captains Mode",
    3: "Single Draft",
    4: "Random Draft",
    5: "All Random",
}

LEAVER_STATUS = {
    None: "Bot",
    "NULL": "Bot",
    0: "Stayed entire match",
    1: "Left after game was safe to leave",
    2: "Abandoned the game"
}


def load_heroes():
    """
    Load hero details from JSON file into memoy
    """

    filename = os.path.join(os.path.dirname(__file__), "data", "heroes.json")

    with open(filename) as f:
        heroes = json.loads(f.read())["result"]["heroes"]
        for hero in heroes:
            HEROES_CACHE[hero["id"]] = hero


def load_items():
    """
    Load item details fom JSON file into memory
    """

    filename = os.path.join(os.path.dirname(__file__), "data", "items.json")

    with open(filename) as f:
        items = json.loads(f.read())["result"]["items"]
        for item in items:
            ITEMS_CACHE[item["id"]] = item


def get_hero_name(id):
    """
    Get hero details from a hero id
    """

    if not HEROES_CACHE:
        load_heroes()

    return HEROES_CACHE.get(id)


def get_item_name(id):
    """
    Get item details fom an item id
    """

    if not ITEMS_CACHE:
        load_items()

    return ITEMS_CACHE.get(id)


def get_steam_id_32(steamid_64):
    """
    Get the 32 bit steam id from the 64 bit version
    """
    return steamid_64 - 76561197960265728


def get_steam_id_64(steamid_32):
    """
    Get the 64 bit steam id from the 32 bit version
    """
    return steamid_32 + 76561197960265728

