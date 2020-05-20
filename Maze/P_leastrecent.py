
from random import randrange, shuffle, choice

#
# actions:
#    0 - do nothing     [0]
#    1 - look,scan..    [1]
#    2 - move           [2,0..3]  0..3 -> east, north, west, south
#

WALL = 100
GOLD =  10

class Explorer:

   def __init__(self,view):
      self.ticker = 0
      self.dm = [1,2,3,0]
      self.view     = view
      self.map = {}
      self.map[(0,0)] = 1
      self.rx = self.ry = 0
      self.tick = 1

   def bestmove(self, view):
      dx = [1,0,-1,0]
      dy = [0,-1,0,1]
      best = 0x7fffffff
      for i in range(4):
         if view[i] < WALL:
            x = self.rx + dx[i]
            y = self.ry + dy[i]
            if (x,y) in self.map:
               t = self.map[(x,y)]
            else:
               t = 0
            if t < best:
               bestlist = [i]
               best = t
            elif t == best:
               bestlist.append(i)
      if len(bestlist) == 0:
         return 0
      m = choice(bestlist)
      x = self.rx + dx[m]
      y = self.ry + dy[m]
      if (x,y) in self.map:
         self.map[(x,y)] = self.tick
      else:
         self.map[(x,y)] = self.tick
      self.rx = x
      self.ry = y
      return m

   def action(self):
      self.tick += 1
      if all([x >= WALL for x in self.view]):
         return [1,0]
      if GOLD in self.view:
         m = self.view.index(GOLD)
         return [2,m]
      m = self.bestmove(self.view)
      if self.view[m] < WALL:
         return [2,m]
      return [1,0]

   def feedback(self, view):
      self.view = view

