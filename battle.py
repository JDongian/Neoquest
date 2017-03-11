import logging
import act
import items

RISK_THRESHOLD = 0.35


def _at_risk(hp_data):
    (my_hp, my_max), (e_hp, e_max) = hp_data

    if my_hp > my_max * RISK_THRESHOLD:
        # don't heal if more than 50%
        return False
    if my_hp > e_max * RISK_THRESHOLD:
        # don't heal if more than half enemy max hp
        return False
    return True


def battle(s, gdata):
    if gdata['stunned']:
        page = act.do_nothing(s)
    elif _at_risk(gdata['hp']):
        if len(gdata['potions']) == 0:
            page = act.flee(s)
        else:
            # TODO: update gdata to put potions in standard row (name, count, type, _action) format
            potion = items.battle_best_potion(gdata['potions'])
            logging.info("drinking potion ({})".format(potion - 220000))
            page = act.use_potion(s, potion)
    else:
        page = act.attack(s)
    return page
