import logging


R_01 = "444444444411111"
#R_12 = "8877855555555555885877766644644446778855555555" # portal problems
R_12 = "8877855555555555885877766644644446778855555555554" # obo hack
R_23 = "555555558777777777877777677855555555532222222222222222211" # portal problems
R_34 = "55587777853222235877778532222355877787777676678587776444441114114444144122222223" # OK
R_45 = "22146777787855558853222222112214444444466677777777858855555555555322323222222211221441144464444444444"
R_56 = "1"
# 2457
R_07 = "7" * 8 + "6" * 3 + "7" * 5  + "65555885" # TODO: check 7x5
R_78 = "22355535322353"
R_89 = "555"
R_910 = "7" * 5 + "88" + "5" * 6


def _format(route):
    return [int(d) for d in route]


def _invert(route):
    return [9 - d for d in reversed(route)]


class Pather():
    CITY1 = 0
    CAVE1 = 1 # inside cave at level 1
    CAVE2 = 2 # beginning of upper temple
    CAVE3 = 3 # beginning of lower temple
    CAVE4 = 4 # beginning of maze
    CAVE5 = 5 # portal exit after cave maze at level 1
    CAVE0 = 6 # outside cave at level 0
    JUNG1 = 7 # entrance of jung
    JUNG2 = 8 # jung dung 1 entrance
    JUNG3 = 9 # jung dung 2 entrance
    JUNG4 = 10 # jung dung 3 entrance
    LOOP = _format("27")
    # TODO: specify portal usage explicity in a route
    # TODO: replace magic numbers with variable names
    # TODO: don't add to travel_queue for loop, instead have a dedicated loop(pos) method
    # TODO: check route efficiency (score based on edge length)
    # TODO: more advanced queuing is needed at the upper level (pathing may be too efficient)
    EDGES = {(0, 0): _format("44" + "27"*4 + "55"),
             (0, 1): _format(R_01),
             (1, 0): _invert(_format(R_01)),
             (1, 1): LOOP,
             (1, 2): _format(R_12),
             (2, 1): _invert(_format(R_12)),
             (2, 2): LOOP,
             (2, 3): _format(R_23),
             (3, 2): _invert(_format(R_23)),
             (3, 3): LOOP,
             (3, 4): _format(R_34),
             (4, 3): _invert(_format(R_34)),
             (4, 4): LOOP,
             (4, 5): _format(R_45),
             (5, 5): LOOP,
             (5, 6): _format(R_56),
             (6, 5): _invert(_format(R_56)),
             (6, 6): LOOP,
             (7, 7): LOOP,
             (8, 8): LOOP,
             (9, 9): LOOP,
             (10, 10): LOOP,
             (1, 6): [],
             (6, 1): [],
             (0, 6): _format(R_01),
             (6, 0): _invert(_format(R_01)),
             (0, 7): _format(R_07),
             (7, 0): _invert(_format(R_07)),
             (7, 8): _format(R_78),
             (8, 7): _invert(_format(R_78)),
             (8, 9): _format(R_89),
             (9, 8): _invert(_format(R_89)),
             (9, 10): _format(R_910),
             (10, 9): _invert(_format(R_910))
            }
    PORTALS = {(0, 1): (None, 1),
               (1, 0): (1, None),
               (1, 2): (None, 2),
               (2, 1): (2, None),
               (2, 3): (None, 4),
               (3, 2): (4, None),
               (3, 4): (None, 6),
               (4, 3): (6, None),
               (4, 5): (None, 8),
               (5, 6): (None, 1),
               (6, 5): (1, None),
               (1, 6): (1, None),
               (6, 1): (None, 1),
               (0, 6): (None, None),
               (6, 0): (None, None),
               (0, 7): (None, 2),
               (7, 0): (1, None),
               (7, 8): (None, 3),
               (8, 7): (1, None),
               (8, 9): (None, 2),
               (9, 8): (4, None),
               (9, 10): (None, 5),
               (10, 9): (29, None)
              }


    def __init__(self, pos):
        #self.is_looping = False # TODO: deadcode
        self.index = 0
        self.route = None
        self.portal = None
        self.pos = pos
        self.dst = None
        self.traveling = False
        self.travel_queue = []


    def get_location(self):
        return self.pos


    def get_destination(self):
        if len(self.travel_queue) == 0:
            return self.dst
        return self.travel_queue[0]


    def _waypoints(self, frm, to, visited):
        if frm == to:
            logging.warn("self-edge used for {}".format(frm))
            return []
        if (frm, to) in self.EDGES:
            logging.debug("edge found for {}->{}".format(frm, to))
            return [frm]

        visited.add(frm)
        logging.debug("visited: {} (+{})".format(visited, frm))
        candidates = []
        for src, dst in self.EDGES:
            if src == frm and not dst in visited:
                logging.debug("considering: {}->{} for {}->{}".format(src, dst, frm, to))
                candidates.append((src, dst))

        if not candidates:
            logging.debug("no path found from: {}".format(frm))
            return [] # spooky

        for _, dst in candidates:
            trial = self._waypoints(dst, to, visited)
            if trial and len(trial) >= 1:
                return [frm] + trial


    def waypoints(self, frm, to):
        return self._waypoints(frm, to, set())[1:]


    def travel(self, dst):
        self.travel_queue.append(dst)


    def next_direction(self):
        if self.dst == None:
            if len(self.travel_queue) == 0:
                # send ourselves in circles
                logging.warn("queried direction without destination")
                logging.info("traveling in circles")
                self.travel(self.pos)
                return self.next_direction()

            next_dst = self.travel_queue[0]

            if (self.pos, next_dst) in self.EDGES:
                # TODO:deadcode self.is_looping = self.pos == next_dst
                self.index = 0
                self.route = self.EDGES[(self.pos, next_dst)]
                self.portal = self.PORTALS.get((self.pos, next_dst), (None, None))
                self.pos = None
                self.dst = next_dst
                self.traveling = True
                self.travel_queue = self.travel_queue[1:]
                logging.debug("travel queue update: {}(-{})".format(self.travel_queue, self.dst))

                return self.next_direction()
            else:
                logging.debug("generating path {}->{}".format(self.pos, next_dst))
                for waypoint in reversed(self.waypoints(self.pos, next_dst)):
                    self.travel_queue.insert(0, waypoint)
                return self.next_direction()

        if self.index == len(self.route):
            logging.info("finishing route to {}".format(self.dst))
            _, portal = self.portal
            self.index = 0
            self.route = None
            self.portal = None
            self.pos = self.dst
            self.dst = None
            self.traveling = False

            if portal:
                return 0, portal
            else:
                return self.next_direction()

        if self.traveling:
            logging.debug("route index: {}".format(self.index))

            portal, portal_end = self.portal
            if portal and self.index == 0:
                self.portal = None, portal_end
                return 0, portal

            d = self.route[self.index]
            self.index += 1
            return d, None
