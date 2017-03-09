import logging
from skill import get_next_code


DIR = {'northwest': 1,
       'north': 2,
       'northeast': 3,
       'west': 4,
       'east': 5,
       'southwest': 6,
       'south': 7,
       'southeast': 8}
URL = "http://www.neopets.com/games/neoquest/neoquest.phtml"
# deadcode HEADER_LEVEL_UP = {'Referer': URL + "?action=skill"}

DATA_ATT = {'fact': "attack", 'type': 0}
DATA_END = {'end_fight': 1}



def move(s, movedir):
    logging.info("move: {movedir}".format(movedir=movedir))

    if movedir in DIR:
        movedir = DIR[movedir]

    #return s.get(NAV_URL.format(movedir=movedir))
    return s.get(URL, params={'action': "move", 'movedir': movedir})


def idle(s):
    return s.get(URL)


def attack(s):
    return s.post(URL, data=DATA_ATT)


def begin_fight(s):
    return s.get(URL)


def loot(s):
    return s.get(URL)


def end_fight(s):
    return s.post(URL, data=DATA_END)


def level_up(s, goals):
    code = get_next_code(s, goals)
    page = s.get(URL, params={'skill_choice': code, 'action': "skill"})
    #time.sleep(0.2)
    return s.get(URL, params={'action': "skill", 'skill_choice': code, 'confirm': 1})
