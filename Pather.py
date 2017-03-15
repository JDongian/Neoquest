import logging


R_01 = "444444444411111"
#R_12 = "8877855555555555885877766644644446778855555555" # portal problems
R_12 = "8877855555555555885877766644644446778855555555554" # obo hack
R_23 = "555555558777777777877777677855555555532222222222222222211" # portal problems
R_34 = "55587777853222235877778532222355877787777676678587776444441114114444144122222223" # OK
R_45 = "22146777787855558853222222112214444444466677777777858855555555555322323222222211221441144464444444444"
R_56 = "1"
# 2457
R_07 = "7" * 8 + "6" * 3 + "7" * 5  + "85555885"
R_78 = "22355535322353"
R_89 = "555"
R_910 = "7" * 5 + "88" + "5" * 6
R_1011 = "5" * 4 + "87" + "8" * 5 + "7" * 4 + "8" * 7 + "555" + "3" * 9 + "5" + "2" * 4 + "3" * 4
R_1112 = "5" * 6 + "8" * 5 + "7" * 7 + "6" * 4 + "7" * 3 + "5886777767777887777677" + "66646" + "4" * 9 + "1" + "4" * 3 + "1" * 4 + "6" * 4 + "44111222"
R_J67 = "44221444112322233555588833588777788323223355538877777"
R_J70 = "7" * 4
R_1310 = "14"
R_C12 = "1"
R_V0S1 = "4" * 11 + "66" + "4" * 11 + "6664676666667"
R_S10 = "644"
R_S1D1 = "888877777"
R_D1R1 = "77777676885553"
R_R12 = "5" * 25 + "335555558"
R_R23 = "5" * 5 + "35535585533323335555885585855553555555333555588777777"
R_R34 = "7" * 15 + "6" + "4" * 38
R_R45 = "7" * 9 + "644676" + "4" * 13 + "6776" + "4" * 11 + "1333233" + "1" * 5 + "412223335335555535553555555553555533355533"
R_RM_01 = "5" * 5 + "3" * 3 + "5" * 3 + "877"
R_RM_12 = "223555333" + "5" * 6 + "333353333" + "33"
R_RM_23 = "6" * 8 + "7" * 26 + "6" + "4" * 5 + "111"
R_RM_34 = "886" + "4" * 5 + "1" + "2" * 12 + "3333" + "2" * 7 + "353" + "2" * 6 + "144"
R_RM_45 = "55" + "8" * 6 + "7888788855553" + "33"
R_RM_56 = "66" + "6664444466444444441223" + "33"
R_RM_60 = "66" + "67785555555533555555555587776" + "6776444441222223555877646"
R_R01 = "4"
R_R1T0 = "7" * 11
R_ERIK = "644"
R_IRGO = "64"
R_T01 = "8"


def _format(route):
    return [int(d) for d in route]


def _invert(route):
    return [9 - d for d in reversed(route)]


class Pather():
    # why is this so bad
    # TODO: str name mapping
    CITY2 = 100 # boris the healer
    CITY1 = 0
    CAVE0 = 6 # outside cave at level 0
    CAVE1 = 1 # inside cave at level 1
    CAVE2 = 2 # beginning of upper temple
    CAVE3 = 3 # beginning of lower temple
    CAVE4 = 4 # beginning of maze
    CAVE5 = 5 # portal exit after cave maze at level 1
    JUNG1 = 7 # jung entrance
    JUNG2 = 8 # jung dung 1 entrance
    JUNG3 = 9 # jung dung 2 entrance
    JUNG4 = 10 # jung dung 3 entrance
    JUNG5 = 11 # jung dung 3 top left right corner -1
    JUNG6 = 12 # jung dung 3 below npc
    JUNG7 = 13 # jung grind before portal
    JUNG0 = 14 # jung dung after portal
    SWMP0 = 15 # swamp city (hills?)
    SWMP1 = 17 # swamp level 0 grinding waypoint
    DSRT1 = 20 # desert level 0 grinding
    TROO1 = 21 # roo level 1 entrance
    TROO2 = 22 # roo level 1 erik waypoint
    TROO3 = 23 # roo level 1 main floor
    TROO4 = 24 # roo level 1 after runs
    NPC04 = 204 # roo level 1 erik
    TRMZ0 = 30 # roo level 2 entrance
    TRM11 = 31 # roo level 2 room 1 (door 1 nexist)
    TRM12 = 32 # roo level 2 room 2
    TRM13 = 33 # roo level 2 room 3
    TRM14 = 34 # roo level 2 room 4
    TRM15 = 35 # roo level 2 room 5
    TRM16 = 36 # roo level 2 room 6
    #TRM16 = 37 # roo level 2 room 7
    TROO0 = 37 # roo after level 2 portal
    TECH1 = 40 # techo plains level 0 grinding
    TECC1 = 41 # techo caves level 1 entrance
    NPC05 = 205 # techo caves level 1 irgo

    LOOP0 = _format("9")
    LOOP1 = _format("7" + "9" * 4 + "2")
    LOOP2 = _format("5" + "9" * 4 + "4")
    LOOP3 = _format("4" + "9" * 4 + "5")
    LOOP4 = _format("44" + "9" * 4 + "55")

    LOOPS = {CITY1: LOOP4,
             CITY2: LOOP3,
             CAVE1: LOOP1,
             CAVE2: LOOP1,
             CAVE3: LOOP1,
             CAVE4: LOOP1,
             CAVE5: LOOP1,
             CAVE0: LOOP1,
             JUNG1: LOOP1,
             JUNG2: LOOP1,
             JUNG3: LOOP1,
             JUNG4: LOOP2,
             #SWMP0: LOOP2,
             TRMZ0: LOOP2
            }
    EDGES = {(CITY1, CITY2): _format(R_C12),
             (CITY1, CAVE1): _format(R_01),
             (CAVE1, CAVE2): _format(R_12),
             (CAVE2, CAVE3): _format(R_23),
             (CAVE3, CAVE4): _format(R_34),
             (CAVE4, CAVE5): _format(R_45),
             (CAVE5, CAVE4): None,
             (CAVE5, CAVE0): _format(R_56),
             (CAVE1, CAVE0): [],
             (CITY1, CAVE0): _format(R_01),
             (CITY1, JUNG1): _format(R_07),
             (JUNG1, JUNG2): _format(R_78),
             (JUNG2, JUNG3): _format(R_89),
             (JUNG3, JUNG4): _format(R_910),
             (JUNG4, JUNG5): _format(R_1011),
             (JUNG5, JUNG6): _format(R_1112),
             (JUNG6, JUNG7): _format(R_J67),
             (JUNG7, JUNG0): _format(R_J70),
             (JUNG0, JUNG7): None,
             (JUNG0, JUNG4): _format(R_1310),
             (JUNG4, JUNG0): None,
             (CAVE0, SWMP1): _format(R_V0S1),
             (SWMP1, SWMP0): _format(R_S10),
             (SWMP1, DSRT1): _format(R_S1D1),
             (DSRT1, TROO1): _format(R_D1R1),
             (TROO1, TROO2): _format(R_R12),
             (TROO2, TROO3): _format(R_R23),
             (TROO2, NPC04): _format(R_ERIK),
             (TROO3, TROO4): _format(R_R34),
             (TROO4, TRMZ0): _format(R_R45),
             (TRMZ0, TRM11): _format(R_RM_01),
             (TRM11, TRM12): _format(R_RM_12),
             (TRM12, TRM13): _format(R_RM_23),
             (TRM13, TRM14): _format(R_RM_34),
             (TRM14, TRM15): _format(R_RM_45),
             (TRM15, TRM16): _format(R_RM_56),
             (TRM16, TROO0): _format(R_RM_60),
             (TROO0, TRM16): None,
             (TROO0, TROO1): _format(R_R01),
             (TROO1, TECH1): _format(R_R1T0)
             (TECC1, NPC05): _format(R_IRGO),
            }
    for src, dst in list(EDGES.keys()):
        if not (dst, src) in EDGES:
            EDGES[(dst, src)] = _invert(EDGES[(src, dst)])
    EDGES = {k: v for k, v in EDGES.items() if v}
    PORTALS = {(CITY1, CAVE1): (None, 1),
               (CAVE1, CITY1): (1, None),
               (CAVE1, CAVE2): (None, 2),
               (CAVE2, CAVE1): (2, None),
               (CAVE2, CAVE3): (None, 4),
               (CAVE3, CAVE2): (4, None),
               (CAVE3, CAVE4): (None, 6),
               (CAVE4, CAVE3): (6, None),
               (CAVE4, CAVE5): (None, 8),
               (CAVE5, CAVE0): (None, 1),
               (CAVE0, CAVE5): (1, None),
               (CAVE1, CAVE0): (1, None),
               (CAVE0, CAVE1): (None, 1),
               (CITY1, JUNG1): (None, 2),
               (JUNG1, CITY1): (1, None),
               (JUNG1, JUNG2): (None, 3),
               (JUNG2, JUNG1): (1, None),
               (JUNG2, JUNG3): (None, 2),
               (JUNG3, JUNG2): (4, None),
               (JUNG3, JUNG4): (None, 5),
               (JUNG4, JUNG3): (29, None),
               (JUNG7, JUNG0): (None, 30),
               (DSRT1, TROO1): (None, 3),
               (TROO1, DSRT1): (3, None),
               (TROO4, TRMZ0): (None, 6),
               (TRMZ0, TROO4): (1, None),
               (TRM16, TROO0): (None, 2),
               (TECH1, TROO1): (None, 3),
               (TROO1, TECH1): (3, None),
               (TECH1, TECC1): (None, 4),
               (TECC1, TECH1): (1, None),
              }


    def __init__(self, pos):
        #self.is_looping = False # TODO: deadcode
        self.index = 0
        self.route = None
        self.portal = None, None
        self.pos = pos
        self.dst = None
        #self.traveling = False # weird variable, indicates if is changing position
        self.travel_queue = []


    def _waypoints(self, frm, to, visited):
        if frm == to:
            logging.critical("self-edge used for {}".format(frm))
            return [frm]
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

        paths = []
        for _, dst in candidates:
            trial = [frm] + self._waypoints(dst, to, visited.copy())
            if trial and len(trial) >= 2:
                paths.append(trial)

        if paths:
            logging.debug("best path for {}->{} is {}".format(frm, to, min(paths, key=lambda p: len(p))))
        else:
            logging.debug("no path for {}->{}".format(frm, to))

        return min(paths, key=lambda p: len(p)) if paths else []


    # begs to be memoized
    def waypoints(self, frm, to):
        return self._waypoints(frm, to, set())[1:]


    def travel(self, dst):
        logging.debug("append travel: {} (+{})".format(self.travel_queue, dst))
        self.travel_queue.append(dst)


    def detour(self, dst):
        logging.debug("detour travel: {} (+{})".format(self.travel_queue, dst))
        self.travel_queue.insert(0, dst)


    def next_direction(self):
        if self.dst is None:
            if len(self.travel_queue) == 0:
                logging.info("circling due to no destination")
                return 9, None

            next_dst = self.travel_queue[0]

            if self.pos == next_dst:
                # TODO:deadcode self.is_looping = True
                self.index = 0
                self.route = self.LOOPS.get(self.pos, self.LOOP0)
                self.portal = None, None
                self.dst = next_dst
                #self.traveling = True
                self.travel_queue = self.travel_queue[1:]
                logging.debug("waypoint update (looping) {}(-{})".format(self.travel_queue, self.dst))
                return self.next_direction()
            elif (self.pos, next_dst) in self.EDGES:
                self.index = 0
                self.route = self.EDGES[(self.pos, next_dst)]
                self.portal = self.PORTALS.get((self.pos, next_dst), (None, None))
                self.dst = next_dst
                #self.traveling = True
                self.travel_queue = self.travel_queue[1:]
                logging.debug("waypoint update {}(-{})".format(self.travel_queue, self.dst))
                return self.next_direction()
            else:
                logging.debug("generating path {}->{}".format(self.pos, next_dst))
                for waypoint in reversed(self.waypoints(self.pos, next_dst)):
                    self.travel_queue.insert(0, waypoint)
                return self.next_direction()

        if self.index == len(self.route):
            _, portal = self.portal
            self.index = 0
            self.route = None
            self.portal = None, None
            self.pos = self.dst
            self.dst = None

            if portal:
                return 0, portal
            else:
                return self.next_direction()

        #if self.traveling:
        logging.debug("route index is {}".format(self.index))

        self.pos = None
        portal, portal_end = self.portal
        if portal and self.index == 0:
            self.portal = None, portal_end
            return 0, portal

        d = self.route[self.index]
        self.index += 1
        return d, None
