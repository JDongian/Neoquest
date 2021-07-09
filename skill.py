import logging
from page_parser import parse_skills

SKILL_CODES = {
        'Fire Weapons': 1001,
        'Firepower': 1002,
        'Fire Ball': 1003,
        'Wall of Flame': 1004,
        'Ice Weapons': 2001,
        'Heart of Ice': 2002,
        'Snowball': 2003,
        'Glacier Strike': 2004,
        'Shock Weapons': 3001,
        'Disable': 3002,
        'Fortitude': 3003,
        'Shockwave': 3004,
        'Spectral Weapons': 4001,
        'Evasion': 4002,
        'Absorption': 4003,
        'Reflex': 4004,
        'Life Weapons': 5001,
        'Field Medic': 5002,
        'Lifesteal': 5003,
        'Resurrection': 5004}
URL_SKILLS = "http://www.neopets.com/games/neoquest/neoquest.phtml?action=skill"


def get_next_code(s, goals):
    parse_skills(s.get(URL_SKILLS).content)
    skill = 'Life Weapons'
    #TODO: logic
    logging.debug("level up: {skill}".format(skill=skill))
    return SKILL_CODES[skill]
