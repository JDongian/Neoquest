import argparse
import time
import logging
import utils
import act
from page_parser import parse_page, page_trim

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
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

    flip = 1

    logging.info("start")
    page = act.idle(s)
    while True:
        game = parse_page(page.content)
        utils.tick_delay()

        # TODO: oop
        if game['state'] == "attack":
            logging.info("battling")
            page = act.attack(s)
        elif game['state'] == "begin_fight":
            logging.info("battle start")
            page = act.begin_fight(s)
        elif game['state'] == "loot":
            logging.info("looting")
            page = act.loot(s)
        elif game['state'] == "end_fight":
            logging.info("battle end")
            page = act.end_fight(s)
        elif game['state'] == "map":
            logging.info("moving")
            flip = (flip + 1) % 2
            page = act.move(s, 4 + flip)
        elif game['state'] == "skill":
            logging.info("level up")
            page = act.level_up(s, None)
        else:
            logging.info("unhandled state")
            exit(-1)

        #logname = '/tmp/p' + str(round(time.time() * 10))[6:] + '.html'
        logdata = page_trim(page.content)
        #with open(logname, 'w') as fp:
        #    fp.write(logdata)
        with open('/tmp/p.html', 'w') as fp:
            fp.write(logdata)
