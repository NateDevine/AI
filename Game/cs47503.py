from random import randrange, shuffle
from constants2 import *

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
      self.move=1
      self.needM=0


   def __str__(self):
      return 'Nate Devine'

   def feedback(self, info):
      type, rem = info

      if type == FEEDBACK_VIEW:
         self.view = rem

      elif type == FEEDBACK_GOTHIT:
         self.x, self.y = rem

   def action(self):
     dirs = [0,1,2,3]
     if not self.move: 
       if self.needM:
         for i in dirs:
           if isWall(self.view[i]): continue
           if isPlayer(self.view[i]): return (CMD_SHOOT,i)
           else:
             self.needM=0
             return (CMD_MOVE, i)
       for i in dirs:
         if isPlayer(self.view[i]):
           return(CMD_SHOOT,i)
         if isFullStation(self.view[i]):
           self.needM=1
           return(CMD_MOVE,i)
       return(CMD_REST,0) 
       
     shuffle(dirs) 

     for i in dirs:
        if isPlayer(self.view[i]):
           return (CMD_SHOOT,i)
        if isFullStation(self.view[i]):
           self.move=0
           self.needM=1
           self.x += dx[i]
           self.y += dy[i]
           self.beento[(self.x, self.y)] = True
           return (CMD_MOVE,i)

     for i in dirs:
       if isWall(self.view[i]): continue
       newx = self.x + dx[i]
       newy = self.y + dy[i]
       if (newx,newy) not in self.beento:
          break
     self.x = newx
     self.y = newy
     self.beento[(newx, newy)] = True
     return (CMD_MOVE,i)