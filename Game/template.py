
#
# Dave is mindless.
#

from constants import *

dx = [1,0,-1,0]
dy = [0,-1,0,1]

class Robo:

#
# pno is a small integer
# energy is (hopefully) larger integer
# pos is a tuple (x,y) giving your current coordinate position
# dim gives the dimensions of the board (width, height)
#
   def __init__(self, pno, energy, pos, dim):
      pass

# returns the name of your character

   def __str__(self):
      return 'Dave'

   def feedback(self, info):

# feedback always gives us a type and then some other info

      type, rem = info

#
# a view = (right, up, left, down, energy)
#

      if type == FEEDBACK_VIEW:
         self.view = rem

#
# if we just got hit, we get the new x,y position
#
      elif type == FEEDBACK_GOTHIT:
         pass
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

