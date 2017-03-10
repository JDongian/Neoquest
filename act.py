import logging
from skill import get_next_code
from page_parser import parse_items

#POT = {'WEAK': 220000,
#       'STANDARD': 220001,
#       'STRONG': 220002,
#       'GREATER': 220003,
#       'SUPERIOR': 220004,
#       'SPIRIT': 220005}
#DIR = {'northwest': 1,
#       'north': 2,
#       'northeast': 3,
#       'west': 4,
#       'east': 5,
#       'southwest': 6,
#       'south': 7,
#       'southeast': 8}
BASE_URL = "http://www.neopets.com/games/neoquest/"
URL = "http://www.neopets.com/games/neoquest/neoquest.phtml"
# deadcode HEADER_LEVEL_UP = {'Referer': URL + "?action=skill"}

DATA_ATT = {'fact': "attack", 'type': 0}
DATA_NOP = {'fact': "noop", 'type': 0}
DATA_END = {'end_fight': 1}
DATA_HUNT = {'movetype': 2}
DATA_SNEAK = {'movetype': 3}
DATA_POT = {'fact': "item", 'type': 220000}


def _worst_potion(items):
    potions = []
    for item in items:
        if 'potion' == item['type'][0]:
            potions.append(item)
    return min(potions, key=lambda p: p['type'][1])


def move(s, movedir, p):
    if p:
        return portal(s, p)

    # if movedir in DIR:
    #     movedir = DIR[movedir]

    return s.get(URL, params={'action': "move", 'movedir': movedir})


def portal(s, p):
    """go through a portal to a different map level"""
    return s.get(URL, params={'action': "move", 'movelink': p})


# higher level function, probably move to grind
# TODO: take in hp param (less visit spam = faster)
def heal(s, hp, overheal=False):
    """heal to full using weakest potions"""
    hp_curr, hp_max = hp
    hp_diff = hp_max - hp_curr
    items = parse_items(s.get(URL, params={'action': "items"}).content)
    potion = _worst_potion(items)
    # TODO: an algorithm using all available potions
    # TODO: consider overheal
    count = min(hp_diff // potion['type'][1], potion['count'][0])

    for _ in range(count):
        logging.info("drinking potion (+{})".format(potion['type'][1]))
        s.get(BASE_URL + potion['action'])
        # time.sleep(1)


def idle(s):
    return s.get(URL)


def grind(s):
    """hack that allows encounters without moving"""
    return s.get(URL + "?action=move&movedir=")


def mode_hunt(s):
    return s.get(URL, params=DATA_HUNT)


def mode_sneak(s):
    return s.get(URL, params=DATA_SNEAK)


def attack(s):
    return s.post(URL, data=DATA_ATT)


def use_potion(s, potency):
    data = DATA_POT
    data['type'] = potency
    return s.post(URL, data=DATA_POT)


def do_nothing(s):
    return s.post(URL, data=DATA_NOP)


def begin_fight(s):
    return s.get(URL)


def loot(s):
    return s.get(URL)


def end_fight(s):
    return s.post(URL, data=DATA_END)


# higher level function
def level_up(s, goals):
    code = get_next_code(s, goals)
    page = s.get(URL, params={'skill_choice': code, 'action': "skill"})
    #time.sleep(0.2)
    return s.get(URL, params={'action': "skill", 'skill_choice': code, 'confirm': 1})
