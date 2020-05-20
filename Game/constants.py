
NPLAYERS      =    4

CMD_REST      =    1
CMD_MOVE      =    2
CMD_PROBE     =    3
CMD_SHOOT     =    4

ENERGY_REST   =    1
ENERGY_MOVE   =   10
ENERGY_PROBE  =    3
ENERGY_SHOOT  =   25

ESTATION      =  0x0010
FSTATION      =  0x0020
STATIONMASK   =  0x0030
PLAYERKEY     =  0x0100
PLAYERMASK    =  0x0f00
WALL          =  0x1000

FEEDBACK_VIEW   =  1
FEEDBACK_FUEL   =  2
FEEDBACK_HIT    =  3
FEEDBACK_MISS   =  4
FEEDBACK_GOTHIT =  5


def isPlayer(x):
   x = x & PLAYERMASK
   return (x >= PLAYERKEY) and (x < WALL)

def isEmptyStation(x):
   x = x & STATIONMASK
   return ((x & ESTATION) != 0)

def isFullStation(x):
   x = x & STATIONMASK
   return ((x & FSTATION) != 0)

def getPlayerNumber(x):
   x = x & PLAYERMASK
   if not isPlayer(x):
      return -1
   for i in range(NPLAYERS):
      if (PLAYERKEY << i) == x:
         return i
   return -1

