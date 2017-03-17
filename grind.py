import argparse
import time
import logging
import utils
import act
import battle
from page_parser import parse_page, page_trim
from Pather import Pather

# TODO: log encounters
M_ROO = ["ghastly initiate",
         "ghastly adept",
         "ghastly priest",
         "ghastly master",
         "ghastly archon",
         "ghastly templar"]

#SKILL_GOALS = {
#    'Life Weapons': 10,
#    'Field Medic': 1,
#    'Lifesteal': 1,
#    'Ice Weapons': 1,
#    'Heart of Ice': 1,
#    'Shock Weapons': 9,
#    'Disable': 9,
#    'Fortitude': 9,
#    'Shockwave': 9
#}

#SKILL_GOALS = {
#    'Life Weapons': 10,
#    'Field Medic': 1,
#    'Lifesteal': 1,
#    'Ice Weapons': 1,
#    'Heart of Ice': 1,
#    'Spectral Weapons': 1,
#    'Evasion': 1,
#    'Absorption': 1,
#    'Reflex': 1,
#    'Shock Weapons': 8,
#    'Disable': 8,
#    'Fortitude': 8,
#    'Shockwave': 8
#}
SKILL_GOALS = {
    'Spectral Weapons': 3,
    'Evasion': 3,
    'Absorption': 3,
    'Reflex': 3,
    'Life Weapons': 5,
    'Field Medic': 5,
    'Lifesteal': 5,
    'Shock Weapons': 7,
    'Disable': 7,
    'Fortitude': 7,
    'Shockwave': 7
}
HP_TARGET = 0.95


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start",
                        type=int,
                        help="specify start location (code)")
    parser.add_argument("-d", "--dst",
                        type=int,
                        help="specify end location (code)")
    parser.add_argument("-v", "--verbosity",
                        action="count", default=0,
                        help="increase output verbosity")
    args = parser.parse_args()

    if args.verbosity == 0:
        logging.basicConfig(level=logging.CRITICAL)
    elif args.verbosity == 1:
        logging.basicConfig(level=logging.ERROR)
    elif args.verbosity == 2:
        logging.basicConfig(level=logging.WARN)
    elif args.verbosity == 3:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(format='\x1b[31m%(levelname)s\x1b[39m:%(message)s', level=logging.DEBUG)

    return args


def get_next_dst(p, maze_lvl):
    if maze_lvl == 0:
        return p.TRM11
    if maze_lvl == 1:
        return p.TRM12
    if maze_lvl == 2:
        return p.TRM13
    if maze_lvl == 3:
        return p.TRM14
    if maze_lvl == 4:
        return p.TRM15
    if maze_lvl == 5:
        return p.TRM16
    if maze_lvl == 6:
        return p.TROO0

    return p.pos


if __name__ == '__main__':
    args = init()

    s = utils.login()
    if not s:
        exit(-1)

    pather = Pather(args.start)
    pather.travel(args.dst)

    logging.info("start")
    page = act.mode_sneak(s)

    roo_maze_lvl = 7

    next_dst = args.dst

    while True:
        game = parse_page(page.content)
        logging.debug("gstate={}".format(game))
        utils.tick_delay()

        # TODO: oop
        if game['state'] == "attack":
            if roo_maze_lvl < 6:
                # roo keys not all obtained
                if M_ROO[roo_maze_lvl] in game['data']['names'][1]:
                    logging.debug("roo_maze++")
                    roo_maze_lvl += 1

            logging.debug("battling {}".format(game['data']['names'][1]))
            page = battle.battle(s, game['data'])
        elif game['state'] == "begin_fight":
            logging.info("battle start")
            page = act.begin_fight(s)
        elif game['state'] == "loot":
            logging.debug("looting")
            page = act.loot(s)
        elif game['state'] == "end_fight":
            logging.info("battle end")
            page = act.end_fight(s)
        elif game['state'] == "skill":
            logging.info("level up")
            page = act.level_up(s, None)
        elif game['state'] == "map":
            # default state, includes dialog (rip)

            # this deserves its own state
            if pather.pos == pather.CITY2:
                act.heal_boris(s)

            heal_count = act.heal(s, game['data']['hp'], HP_TARGET)

            # disgusting
            hp_curr, hp_max = game['data']['hp']
            if heal_count == 0 and hp_curr / hp_max < 0.4: # TODO: help
                # go to boris
                logging.info("low hp and low potions so sneaking to boris")
                act.mode_sneak(s)
                p.detour(p.CITY2)


            # also rip, should be abstracted
            # TODO: debug
            if len(pather.travel_queue) == 0:
                logging.info("travel queue empty and pos={}".format(pather.pos))
                #next_dst = get_next_dst(pather, roo_maze_lvl) # eventually add back
                #if pather.pos != next_dst:
                #    logging.info("but not reached destination {}".format(next_dst))
                #    pather.travel(next_dst)
                #    act.mode_sneak(s) # eventually remove

            if pather.pos == next_dst:
                logging.info("reached destination")
                act.mode_hunt(s) # eventually replace with sneak many mode

            direction, p = pather.next_direction()
            #exit(0) # debug pathing
            logging.info("move: {} {}".format(direction, p))
            page = act.move(s, direction, p)
        else:
            logging.critical("unhandled state")
            exit(-1)

        logdata = page_trim(page.content)
        #logdata = page.content.decode('utf-8')
        with open('/tmp/p.html', 'w') as fp:
            fp.write(logdata)
        if args.verbosity == 4:
            logname = '/tmp/p' + str(round(time.time() * 10))[7:] + '.html'
            with open(logname, 'w') as fp:
                fp.write(logdata)


