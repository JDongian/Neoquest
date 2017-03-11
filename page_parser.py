import re
from bs4 import BeautifulSoup


E_INFO = {'name': "div",
            'attrs': {'style': "padding:7px;", 'align':"center"}}
E_SKILL = {'name': "div",
             'attrs': {'class': "contentModule phpGamesNonPortalView"}}
E_ITEMS = {'name': "table",
           'attrs': {'border': 1, 'cellspacing': 0, 'cellpadding': 3}}

ID_ATT = """Weapon: """
ID_SKILL = """** Spend Skill Points ***"""
ID_BEG = """Click here to begin the fight!"""
ID_LOOT = """ to see what you found!"""
ID_END = """Click here to return to the map"""
RE_POT = """, (\\d+)\\); return false;">U.+?Potion \(heals (\d+)\) \((\d+) l"""


def parse_page(html):
    """determine what is happening in the game
    States: battle (fighting), map (moving), talk (talking)
    """
    parsed_html = BeautifulSoup(html, "html.parser")
    info = parsed_html.body.find(**E_INFO)
    text = info.decode()

    hp = re.findall("Health:.*?(\d+).*?(\d+)", text)
    if len(hp) == 1:
        hp = map(int, hp[0])
    else:
        (my_hp, my_max), (e_hp, e_max) = hp[1:]
        my_hp, my_max, e_hp, e_max = map(int, (my_hp, my_max, e_hp, e_max))
        hp = (my_hp, my_max), (e_hp, e_max)

    data = {'state': "map", 'data': {'hp': hp}}

    if ID_ATT in text:
        names = [e.next.next for e in info.find_all('font')]
        stunned = text.find(">Attack</a>") == -1
        potions = [[int(e) for e in res] for res in re.findall(RE_POT, text)]
        data['data'].update({'names': names,
                             'stunned': stunned,
                             'potions': potions})
        data['state'] = "attack"
    elif ID_BEG in text:
        data['state'] = "begin_fight"
    elif ID_LOOT in text:
        # TODO: test if can shortcut past this without losing loot
        data['state'] = "loot"
    elif ID_END in text:
        data['state'] = "end_fight"
    elif ID_SKILL in text:
        data['state'] = "skill"
    #else:
    #    data['state'] = "map"

    return data


def parse_skills(html):
    parsed_html = BeautifulSoup(html, "html.parser")
    info = parsed_html.body.find(**E_SKILL)
    text = info.decode()
    # TODO: implement


def parse_items(html):
    parsed_html = BeautifulSoup(html, "html.parser")
    info = parsed_html.body.find(**E_ITEMS)
    rows = [[e.contents for e in row.find_all('td')] for row in info.find_all('tr')[1:]]

    results = []
    # TODO: WIP
    for row in rows:
        name, count, item_type, action = row
        if 'Potion' in item_type[0].decode():
            heal = int(re.search('\d+', item_type[0].contents[1]).group())
            results.append({'name': name[0].next,
                            'count': (int(count[0].next), int(count[1][1:])),
                            'type': ("potion", heal),
                            'action': action[0].attrs['href']})
    return results


def page_trim(html):
    parsed_html = BeautifulSoup(html, "html.parser")
    info = parsed_html.body.find(**E_SKILL)
    return info.decode()
