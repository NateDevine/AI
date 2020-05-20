
#
# Carol is a basic player, no real strategy, just does some of the
# basic things.
#

from random import randrange, shuffle
from constants import *

dx = [1,0,-1,0]
dy = [0,-1,0,1]

class Robo:

   def __init__(self, pno, energy, pos, dim):
      self.beento = {}
      self.tick = 0
      self.pno = pno
      self.energy = energy
      self.x, self.y = pos
      self.wid, self.hgt = dim
      self.beento[pos] = True

   def __str__(self):
      return 'Carol'

   def feedback(self, info):
      type, rem = info
#
# if this is a VIEW, save the VIEW
#
      if type == FEEDBACK_VIEW:
         self.view = rem
#
# if we just got hit, save our new position
#
      elif type == FEEDBACK_GOTHIT:
         self.x, self.y = rem

   def action(self):
#
# shuffle the list of directions
#
      dirs = [0,1,2,3]
      shuffle(dirs)
#
# first check for other players and fuel stations
#
      for i in dirs:
         if isPlayer(self.view[i]):
            return (CMD_SHOOT,i)
         if isFullStation(self.view[i]):
            self.x += dx[i]
            self.y += dy[i]
#
# this would be a good time to remember where this fuel station is located
#
            self.beento[(self.x, self.y)] = True
            return (CMD_MOVE,i)
#
# next check places we haven't seen, if we find one, break out of the loop
#
      for i in dirs:
         if self.view[i] == WALL:
            continue
         newx = self.x + dx[i]
         newy = self.y + dy[i]
         if (newx,newy) not in self.beento:
            break
      self.x = newx
      self.y = newy
      self.beento[(newx, newy)] = True
      return (CMD_MOVE,i)

