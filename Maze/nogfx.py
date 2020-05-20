#!/usr/bin/env python3
  
import sys
import time
from random import randrange, shuffle
from makemaze import Maze
from statistics import median

# Your module goes here: explorerXX

from explorer03 import Explorer as Explorer1

NPLAYER =   1
GAMEWID =  12
GAMEHGT =  12
WALL    = 100

ExplorerList = [Explorer1]

class Player:

   def __init__(self, game, pno):
      self.pno = WALL + 1 + pno
      self.game = game
      self.brd = game.board
      self.x   = 0
      self.y   = 0
      self.brd[self.x][self.y] = self.pno

   def move(self, x, y):
      self.brd[x][y] = self.pno
      self.brd[self.x][self.y] = 0
      self.x = x
      self.y = y

class Game:

   def __init__(self, rows, cols):
      
      self.rows  = rows
      self.cols  = cols

      self.target = (randrange(cols//2,cols-1),randrange(rows//2,rows-1))

      self.running = False
      self.turn    = 0

      tmp = Maze(cols,rows)
      self.wall = tmp.getwalls()
 
      self.starting = True
      self.reset()
      self.starting = False

   def reset(self):
      self.running = False

      if not self.starting:
         for i in range(NPLAYER):
            self.player[i].move(0,0)

      self.board = []
      for i in range(self.cols):
         self.board.append([0 for j in range(self.rows)])     

      self.player = []
      for i in range(NPLAYER):
         self.player.append(Player(self,i))

      self.explorer = [None] * NPLAYER
      for i in range(NPLAYER):
         self.explorer[i] = ExplorerList[i](0,0,self.target[0],self.target[1])

   def getview(self, x, y):

      dx   = [ 1, 0,-1, 0]
      dy   = [ 0,-1, 0, 1]
      vw = []
      for i in range(4):
         if self.wall[(x,y)][i]:
            vw.append(WALL)
         else:
            vw.append(self.board[x+dx[i]][y+dy[i]])
      return vw

   def cmdHandler(self,who):
      dx   = [1,0,-1,0]
      dy   = [0,-1,0,1]
      x = self.player[who].x
      y = self.player[who].y
      vw = self.getview(x,y)
      self.explorer[who].feedback(vw)
      cmd = self.explorer[who].action()
      if cmd[0] == 2:
         dir = cmd[1]
         x = self.player[who].x
         y = self.player[who].y
         if not self.wall[(x,y)][dir]:
            newx = x+dx[dir]
            newy = y+dy[dir]
            self.player[who].move(newx, newy)
            if (newx,newy) == self.target:
               self.running  = False
         else:
            print('WALL: tried to go', dir, 'from', x, y)
      elif cmd[0] == 1:
         pass
      else:
         print('whoops')

   def playgame(self, printflag):
      ticks = 0
      self.running = True
      while self.running:
         ticks += 1
         self.cmdHandler(self.turn)
         self.turn = (self.turn + 1) % NPLAYER
      if printflag:
         print('target: {0:2d},{1:2d}   ticks: {2:5d}'.format(self.target[0], self.target[1], ticks))
      return ticks
         
if __name__ == '__main__':

   n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
   li = []
   for i in range(n):
      game = Game(GAMEHGT,GAMEWID)
      t = game.playgame(n < 100)
      li.append(t)
   if n != 0:
      print('averaged {0:.3f} moves in {1:d} tries'.format(sum(li)/n, n))
      print('median: ',median(li))
      print('best:  {0:d}\nworst: {1:d}'.format(min(li),max(li)))
