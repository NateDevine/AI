
#
# Dave is mindless.
#

from random import randrange, shuffle
from constants2 import *

dx = [1,0,-1,0]
dy = [0,-1,0,1]

class Robo:

   def __init__(self, pno, energy, pos, dim):
      pass

   def __str__(self):
      return 'Dave'

   def feedback(self, info):
      type, rem = info
#
# if this is a VIEW, save the VIEW
#
      if type == FEEDBACK_VIEW:
         self.view = rem
      else:
         pass

   def action(self):
#
# shuffle the list of directions
#
      dirs = [0,1,2,3]
      shuffle(dirs)
#
# move anywhere we can, but shoot if we happen to see another player
#
      for i in dirs:
         if self.view[i] == WALL:
            continue
         if isPlayer(self.view[i]):
            return (CMD_SHOOT,i)
         return (CMD_MOVE,i)
      return (CMD_REST,0)

