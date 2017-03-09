import logging


DIR = {'northwest': 1,
       'north': 2,
       'northeast': 3,
       'west': 4,
       'east': 5,
       'southwest': 6,
       'south': 7,
       'southeast': 8}
BASE_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml"
NAV_URL = BASE_URL + "?action=move&movedir={movedir}"

ATT_DATA = {'fact': "attack", 'type': 0}


def move(s, movedir):
    logging.info("move: {movedir}".format(movedir=movedir))

    if movedir in DIR:
        movedir = DIR[movedir]

    return s.get(NAV_URL.format(movedir=movedir))


def idle(s):
    return s.get(BASE_URL)


def attack(s):
    return s.post(BASE_URL, data=ATT_DATA)
