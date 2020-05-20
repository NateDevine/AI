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


   def __str__(self):
      return 'Nate'

   def feedback(self, info):
      type, rem = info

      if type == FEEDBACK_VIEW:
         self.view = rem

      elif type == FEEDBACK_GOTHIT:
         self.x, self.y = rem

   def action(self):
     dirs = [0,1,2,3]
     if self.move:
       if randrange(100) < 25:
          return (CMD_PROBE, 0)

       
       shuffle(dirs) 

       for i in dirs:
          if isPlayer(self.view[i]):
             return (CMD_SHOOT,i)
          if isFullStation(self.view[i]):
             self.x += dx[i]
             self.y += dy[i]
             self.beento[(self.x, self.y)] = True
             return (CMD_MOVE,i)
#
# check if we are in an area with walls on all but one side. if we are then start the camping
#
     free=3
     walls=0
     for i in dirs:
        if isWall(self.view[i]):
           walls+=1
           #print(i, ",", walls)
           if walls==3:
             #print("in camping mode")
             self.move=0
             for j in dirs:
               if isPlayer(self.view[j]):
                 print("target aquired, Pure Skill")
                 return (CMD_SHOOT,j)
             return(CMD_REST, 0)
        free=i
     self.move=1      
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