from page_parser import parse_items

# TODO: constants file?
URL = "http://www.neopets.com/games/neoquest/neoquest.phtml"


def _filter_potions(items):
    potions = []
    for item in items:
        if 'potion' == item['type'][0]:
            potions.append(item)
    return potions


def get_items(s):
    return parse_items(s.get(URL, params={'action': "items"}).content)


def get_potions(s):
    return _filter_potions(get_items(s))


def battle_best_potion(potions):
    """return code of best potion found during battle
    parameter: game data['potions']"""
    if len(potions) > 0:
        return max(potions, key=lambda e: e[1])[0]
    else:
        return None


def worst_potion(potions):
    """return code of best potion found during battle
    parameter: potion list from non-combat item list"""
    if len(potions) > 0:
        return min(potions, key=lambda p: p['type'][1])
    else:
        return None
