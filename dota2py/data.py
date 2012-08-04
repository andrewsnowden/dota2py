"""
ID lookups from data files

Thanks to Lazze for the item list:
http://dev.dota2.com/showthread.php?t=47115&page=16&p=296787#post296787
"""

import os.path
import json

HEROES_CACHE = {}
ITEMS_CACHE = {}


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
