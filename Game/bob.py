
from random import randrange, shuffle
from constants import *

dx = [1,0,-1,0]
dy = [0,-1,0,1]

class Robo:
   # def __init__(self, pno, energy, pos, dim):
   def __init__(self, pno, energy, pos, dim):
      self.beento = {}
      self.pno = pno
      self.energy = energy
      self.x = pos[0]
      self.y = pos[1]
      self.beento[(pos[0],pos[1])] = True

   def __str__(self):
      return 'Bob'

   def feedback(self, info):
      type, rem = info
      if type == FEEDBACK_VIEW:
         self.view = rem
      elif type == FEEDBACK_GOTHIT:
         self.x, self.y = rem

   def action(self):
      dirs = [0,1,2,3]
      shuffle(dirs)
      for i in dirs:
         if isPlayer(self.view[i]):
            return (CMD_SHOOT,i)
         if isFullStation(self.view[i]):
            self.x += dx[i]
            self.y += dy[i]
            self.beento[(self.x, self.y)] = True
            return (CMD_MOVE,i)
      for i in dirs:
         if self.view[i] == WALL:
            continue
         newx = self.x + dx[i]
         #print(self.x)
         newy = self.y + dy[i]
         if isFullStation(self.view[i]):
            break
         if (newx,newy) not in self.beento:
            break
      self.x = newx
      self.y = newy
      self.beento[(newx, newy)] = True
      return (CMD_MOVE,i)
     
