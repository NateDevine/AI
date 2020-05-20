
#
# Bob does not use probe, but explores the maze
# more efficiently than Carol.  Bob learns the
# locations of the fuel stations, and heads for
# the least recently visited station when fuel
# is low.
#

from random import randrange, shuffle
from constants2 import *
from pathfinder import dijkstra

dx = [1,0,-1,0]
dy = [0,-1,0,1]
revdir = {(1,0): 0, (0,-1): 1, (-1,0): 2, (0,1): 3}

class Robo:

   def __init__(self, pno, energy, startpos, gamedim):

      self.pno = pno                            # player number
      self.energy = energy                      # fuel
      self.x, self.y = startpos                 # x,y coordinates to start
      self.wid, self.hgt = gamedim              # size of board
      self.minenergy = 1500                     # energy to trigger fuel station search
      self.stations = {}                        # dictionary of stations
      self.dirs = [0,1,2,3]                     # list of directions (to shuffle)
      self.tick = 1                             # move counter
      self.initmap()
      self.beento = {}                          # dictionary for squares we've visited
      for k in self.walls:
         self.beento[k] = 0
      self.beento[startpos] = self.tick         # we've been to the start location

   def __str__(self):
      return 'Bob'
      
   def initmap(self):
      self.walls = {}
      for x in range(self.wid):
         for y in range(self.hgt):
            self.walls[(x,y)] = [ self.nextsquare(x,y,i) == None for i in range(4)]

   def getdir(self, delta):
      if delta in revdir:
         return revdir[delta]
      return None

   def nextsquare(self,x,y,dir):
      if dir == 0 and x == self.wid-1: return None
      if dir == 1 and y == 0: return None
      if dir == 2 and x == 0: return None
      if dir == 3 and y == self.hgt-1: return None
      return (x + dx[dir], y + dy[dir])

   def feedback(self, info):                  # FEEDBACK
      type, rem = info
#
# if this is a VIEW, save the VIEW
#
      if type == FEEDBACK_VIEW:
         if (self.x,self.y) != (rem[5],rem[6]):
            print(self.x,self.y,rem[5],rem[6])
            self.x,self.y != rem[5],rem[6]
         self.view = rem
         self.energy = rem[4]
#
# if we just got hit, save our new position
#
      elif type == FEEDBACK_PROBE:
         pass
      elif type == FEEDBACK_GOTHIT:           # we are moved to random empty square when hit
         self.x, self.y = rem

   def addstation(self, x, y):
      if (x,y) in self.stations:
         self.stations[(x,y)] = self.tick
         return
      self.stations[(x,y)] = self.tick
      print(self.stations.keys())

   def updatemap(self):
      for i in range(4):
         if isWall(self.view[i]) and not self.walls[(self.x, self.y)][i]:
            self.walls[(self.x, self.y)][i] = True
            newsq = self.nextsquare(self.x, self.y, i)
            if newsq:
               self.walls[newsq][(i+2) % 4] = True
#
# move finders: player, stations, unvisited squares, any square
#

   def findplayers(self):
      for i in self.dirs:
         if isPlayer(self.view[i]):
            self.bestmove = (CMD_SHOOT,i)
            return True
      return False

   def findstations(self):
      for i in self.dirs:
         if isFullStation(self.view[i]):
            self.x += dx[i]
            self.y += dy[i]
            self.addstation(self.x, self.y)
            self.beento[(self.x, self.y)] = self.tick
            self.bestmove = (CMD_MOVE,i)
            return True
         elif isEmptyStation(self.view[i]):
            self.addstation(self.x + dx[i], self.y + dy[i])
      return False

   def findnewmove(self):
      for i in self.dirs:
         if isWall(self.view[i]):
            continue
         newx = self.x + dx[i]
         newy = self.y + dy[i]
         if self.beento[(newx,newy)] == 0:
            self.x = newx
            self.y = newy
            self.beento[(newx, newy)] = self.tick
            self.bestmove = (CMD_MOVE,i)
            return True
      return False

   def findgoodmove(self):
      best = self.tick
      move = None
      for i in self.dirs:
         if isWall(self.view[i]):
            continue
         newx = self.x + dx[i]
         newy = self.y + dy[i]
         if self.beento[(newx,newy)] < best:
            best = self.beento[(newx,newy)]
            move = i
            loc = (newx, newy)
      if move:
         self.x, self.y = loc
         self.beento[loc] = self.tick
         self.bestmove = (CMD_MOVE, move)
         return True
      return False

   def findanymove(self):
      for i in self.dirs:
         if isWall(self.view[i]):
            continue
         newx = self.x + dx[i]
         newy = self.y + dy[i]
         self.x = newx
         self.y = newy
         self.beento[(newx, newy)] = self.tick
         self.bestmove = (CMD_MOVE, i)
         return True
      return False

   def pickstation(self):
      if len(self.stations) < 2:
         return None
      return min(self.stations.keys(), key=lambda k: self.stations[k])

   def getpathmove(self,target):
      path = dijkstra(self.walls, (self.x, self.y), target)
      if len(path) > 1:
         (dx,dy) = (path[1][0] - path[0][0], path[1][1] - path[0][1])
         dir = self.getdir((dx,dy))
         if not isWall(self.view[dir]):
            self.x, self.y = path[1]
            self.bestmove = (CMD_MOVE, dir)
            return True
      return False

   def findfuel(self):
      st = self.pickstation()
      if not st:
         return False
      if self.getpathmove(st):
         return True

   def findnewsquare(self):
      for k in self.beento:
         if self.beento[k] == 0:
            if self.getpathmove(k):
               return True
      return None

   def action(self):                     # ACTION begins here -=-=-=-=-=-=-=-=-

      self.tick += 1
      shuffle(self.dirs)

      self.updatemap()                   # use latest view to update map

      if self.findplayers():             # are we next to a player?
         return self.bestmove

      if self.findstations():            # are we next to a station?
         return self.bestmove

      if self.energy < self.minenergy:   # low on fuel?
         if self.findfuel():             # look for path to a station
            return self.bestmove

      if self.findnewmove():             # go to adjacent unvisited square
         return self.bestmove

      if self.findnewsquare():           # look for path to unvisited square
         return self.bestmove

      if self.findgoodmove():            # take least recently visited square
         return self.bestmove

      if self.findanymove():             # take any square
         return self.bestmove

      return (CMD_REST, 0)

