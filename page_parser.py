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
ID_BEG = """Click here to begin the fight"""
ID_LOOT = """ to see what you found!"""
ID_END = """Click here to return to the map"""
ID_DIE = """Click here to return to Neopia City"""
RE_POT = """, (\\d+)\\); return false;">U.+?Potion \(heals (\d+)\) \((\d+) l"""


def _format_potions(p_arr):
    #print(p_arr)
    # TODO: implement
    return p_arr


def parse_page(html):
    """determine what is happening in the game
    States: battle (fighting), map (moving), talk (talking)
    """
    parsed_html = BeautifulSoup(html, "html.parser")
    info = parsed_html.body.find(**E_INFO)
    text = info.decode()

    hp = re.findall("Health:.*?(\d+).*?(\d+)", text)
    if len(hp) == 1:
        hp = tuple(map(int, hp[0]))
    else:
        (my_hp, my_max), (e_hp, e_max) = hp[1:]
        my_hp, my_max, e_hp, e_max = map(int, (my_hp, my_max, e_hp, e_max))
        hp = (my_hp, my_max), (e_hp, e_max)

    data = {'state': "map", 'data': {'hp': hp}}

    if ID_ATT in text:
        names = [e.next.next for e in info.find_all('font')]
        stunned = text.find(">Attack</a>") == -1
        potions = _format_potions([[int(e) for e in res] for res in re.findall(RE_POT, text)])
        data['data'].update({'names': names,
                             'stunned': stunned,
                             'potions': potions})
        data['state'] = "attack"
    elif ID_BEG in text: #TODO: missing a case or two
        data['state'] = "begin_fight"
    elif ID_LOOT in text:
        data['state'] = "loot"
    elif ID_END in text or ID_DIE in text: #TODO: separate die case
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
        name, count, item_type, action = None, None, None, None
        try:
            # is there a better way to do this
            name, count, item_type, action = row
        except ValueError:
            logging.warn("unparsable row: {}", row)
            continue
        if 'Potion' in item_type[0].decode():
            heal = int(re.search('\d+', item_type[0].contents[1]).group())
            results.append({'name': name[0].next,
                            'count': (int(count[0].next), int(count[1][1:])),
                            'type': ("potion", heal),
                            'action': action[0].attrs['href']})
    return results


def page_trim(html):
    #parsed_html = BeautifulSoup(html, "html.parser")
    #parsed_html.body.find(attrs={'id': 'pushdown_banner'}).extract()
    #parsed_html.body.find(attrs={'id': 'ban'}).extract()
    #parsed_html.body.find(attrs={'id': 'header'}).extract()
    #parsed_html.body.find(attrs={'id': 'footer'}).extract()
    #parsed_html.body.find(attrs={'id': 'pushdown_banner_btf'}).extract()
    #parsed_html.body.find(attrs={'id': 'adsense'}).extract()
    #parsed_html.body.find(attrs={'class': 'sidebar'}).extract()
    #parsed_html.body.find(attrs={'class': 'phpGamesTowerAd'}).extract()

    r =  re.sub("""<div id="pushdown_banner".*<div id="content">""",
                """<div id="content" style="background-color:#FDFDFD">""",
                html.decode(), flags=re.DOTALL)

    r =  re.sub("""<div class="phpGamesTowerAd">.*?div>.*?div>""",
                "", r, flags=re.DOTALL)

    return r
