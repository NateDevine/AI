
from random import randrange, shuffle, choice
from constants import *

dx = [1,0,-1,0]
dy = [0,-1,0,1]

class Robo:

   def __init__(self, pno, energy, pos, dim):
      self.beento = {}
      self.pno = pno
      self.energy = energy
      self.tick = 0
      self.x, self.y = pos
      self.beento[(pos[0],pos[1])] = True

   def __str__(self):
      return 'Alice'

   def feedback(self, info):
      type, rem = info
      if type == FEEDBACK_VIEW:
         self.view = rem
      elif type == FEEDBACK_GOTHIT:
         self.x, self.y = rem

   def action(self):
      self.tick += 1
      dirs = [0,1,2,3]
      shuffle(dirs)
      for i in dirs:
         if isPlayer(self.view[i]):
            return (CMD_SHOOT,i)
         if isFullStation(self.view[i]):
            self.x += dx[i]
            self.y += dy[i]
            self.beento[(self.x, self.y)] = 1
            return (CMD_MOVE,i)
      if self.view[-1] > 1000 and choice([1,2,3]) != 3:
         return (CMD_REST, 0)
      record = 0x7fffffff
      d = -1
      for i in dirs:
         if self.view[i] == WALL:
            continue
         newx, newy = self.x + dx[i], self.y + dy[i]
         if isFullStation(self.view[i]) or ((newx,newy) not in self.beento):
            tx, ty, d = newx, newy, i
            break
         elif self.beento[(newx,newy)] < record:
            record = self.beento[(newx,newy)]
            tx = newx
            ty = newy
            d = i
      self.x, self.y = tx, ty
      self.beento[(tx, ty)] = self.tick
      return (CMD_MOVE,d)
     
