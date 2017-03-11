import argparse
import time
import logging
import utils
import act
import battle
from page_parser import parse_page, page_trim
from Pather import Pather

#SKILL_GOALS = {
#    'Fire Weapons': 7,
#    'Firepower': 7,
#    'Ice Weapons': 7,
#    'Shock Weapons': 7,
#    'Disable': 7,
#    'Fortitude' 7,
#    'Shockwave': 7
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start",
                        type=int, default=-1,
                        help="specify start location (code)")
    parser.add_argument("-d", "--dst",
                        type=int, default=-1,
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

    s = utils.login()
    if not s:
        exit(-1)
    #pather = Pather(Pather.CITY1)
    pather = Pather(args.start)

    logging.info("start")
    #page = act.idle(s)
    page = act.mode_sneak(s)
    while True:
        game = parse_page(page.content)
        logging.debug("gstate={}".format(game))
        utils.tick_delay()

        # TODO: oop
        if game['state'] == "attack":
            logging.debug("battling")
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
            if pather.get_location() == pather.CITY2:
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
            if pather.get_location() == args.dst:
                logging.info("reached destination to grind")
                act.mode_hunt(s)

            if pather.get_destination() == None:
                logging.info("currently no destination so going to arg dst")
                pather.travel(args.dst)
                #pather.travel(args.start)
                #pather.travel(pather.JUNG1)
            direction, p = pather.next_direction()
            exit(0) # debug pathing
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
            logname = '/tmp/p' + str(round(time.time() * 10))[8:] + '.html'
            with open(logname, 'w') as fp:
                fp.write(logdata)


