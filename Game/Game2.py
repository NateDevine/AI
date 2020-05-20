#!/usr/bin/env python3
  
import sys
import time
from random import randrange, shuffle
from tkinter import *
from makemaze import Maze

# Your module goes here: roboXX

# This next line will be replaced by something like:
#
# from cs475XX import Robo as Robo1

from bob2 import Robo as Robo1

from cs47503 import Robo as Robo2

from constants2 import *

NPLAYER       =      2
BORDER        =     10
XUNIT         =     64
YUNIT         =     64

PLAYERSIZE    =     32
STATIONSIZE   =     30

GAMEWID       =     12
GAMEHGT       =     12
NSTATIONS     =      5
TOOCLOSE      =      5
FUEL          =   1000
REFILL        =    200
INITENERGY    =   1000

initposX = [0, GAMEWID-1]
initposY = [0, GAMEHGT-1]

colorlist = ['blue', 'purple2', 'orange', 'slategray']

fueldata = [[FUEL, GAMEWID//2, GAMEHGT//2],
            [FUEL, GAMEWID//4, GAMEHGT//4],
            [FUEL, GAMEWID//4, (3*GAMEHGT)//4],
            [FUEL, (3*GAMEWID)//4, GAMEHGT//4],
            [FUEL, (3*GAMEWID)//4, (3*GAMEHGT)//4]
           ]

energyuse = [0, ENERGY_REST, ENERGY_MOVE, ENERGY_PROBE, ENERGY_SHOOT]

RoboList = [Robo1,Robo2]

class Player:

   def __init__(self, game, pno, x, y):
      self.pno    = pno
      self.mask   = (PLAYERKEY << pno)
      self.energy = INITENERGY
      self.game = game
      self.lab = game.scorelab[pno]
      self.brd = game.board
      self.clock = 0
      self.x   = x
      self.y   = y
      self.brd[self.x][self.y] |= self.mask
      self.px  = BORDER + self.x * XUNIT + XUNIT // 2
      self.py  = BORDER + self.y * YUNIT + YUNIT // 2
      self.me  = game.can.create_oval(self.px - PLAYERSIZE, self.py - PLAYERSIZE,
                                      self.px + PLAYERSIZE, self.py + PLAYERSIZE, fill=colorlist[pno])

   def move(self, x, y):
      self.brd[x][y] ^= self.mask
      self.brd[self.x][self.y] ^= self.mask
      self.x = x
      self.y = y
      self.px  = BORDER + x * XUNIT + XUNIT // 2
      self.py  = BORDER + y * YUNIT + YUNIT // 2
      self.game.can.coords(self.me, self.px - PLAYERSIZE, self.py - PLAYERSIZE, self.px + PLAYERSIZE, self.py + PLAYERSIZE)

   def update(self, delta):
      self.energy += delta
      self.lab.configure(text=str(self.energy))
      return (self.energy >= 0)
         

class Game:

   def __init__(self, win, rows, cols):
      self.win = win
      self.win.option_add("*font",("Helvetica",36))
      self.win.title("Maze")
      
      self.rows  = rows
      self.cols  = cols
      self.xunit = XUNIT
      self.yunit = YUNIT
      self.wid   = cols * self.xunit + 2 * BORDER
      self.hgt   = rows * self.yunit + 2 * BORDER
      self.wallwidth = 3

      self.infoframe = Frame(win)
      self.infoframe.pack(side='top')
      self.dataframe = Frame(win)
      self.dataframe.pack(side='left')
      self.gfxframe  = Frame(win)
      self.gfxframe.pack(side='left')
      self.ctlframe  = Frame(win)
      self.ctlframe.pack(side='left')

      self.info = Label(self.infoframe,text='Welcome to ISU',width=40,height=1,fg='black',bg='lightblue')
      self.info.pack(expand=1)

      self.namelab = []
      self.scorelab = []
      for i in range(NPLAYER):
         lab = Label(self.dataframe,text='Player '+str(i+1),width=5,height=1,fg=colorlist[i])
         lab.pack(side='top')
         self.namelab.append(lab)
         lab = Label(self.dataframe,text=str(INITENERGY))
         lab.pack(side='top')
         self.scorelab.append(lab)

      self.can = Canvas(self.gfxframe, width=self.wid, height=self.hgt, bg='#50c878')  # or wheat
      self.can.pack()

      Button(self.ctlframe, text='Start', command=self.automate).pack(side='top', fill=X)
      Button(self.ctlframe, text='Pause', command=self.stop).pack(side='top', fill=X)
      Button(self.ctlframe, text='Quit', command=win.quit).pack(side='top', fill=X)
      #Button(self.ctlframe, text='Reset', command=self.setup).pack(side='top', fill=X)

      self.win.option_add("*Radiobutton.font",("Helvetica",24))
      self.ticker = IntVar()
      self.ticker.set(25)
      Radiobutton(self.ctlframe, text="See Results", indicatoron = False, variable=self.ticker,
        value=  0).pack(side='top',fill=X)
      Radiobutton(self.ctlframe, text="Speed:    1", indicatoron = False, variable=self.ticker,
         value=  1).pack(side='top',fill=X)
      Radiobutton(self.ctlframe, text="Speed:   25", indicatoron = False, variable=self.ticker,
         value=  25).pack(side='top',fill=X)
      Radiobutton(self.ctlframe, text="Speed:  100", indicatoron = False, variable=self.ticker,
         value= 100).pack(side='top',fill=X)
      Radiobutton(self.ctlframe, text="Speed:  250", indicatoron = False, variable=self.ticker,
         value= 250).pack(side='top',fill=X)
      Radiobutton(self.ctlframe, text="Speed: 1000", indicatoron = False, variable=self.ticker,
         value=1000).pack(side='top',fill=X)

      tmp = Maze(cols,rows)
      self.wall = tmp.getwalls()
      self.make_grid()
 
      self.stuff = {}
      self.setup()

   def makestations(self):

      for i in range(NSTATIONS):
         x = fueldata[i][1] + randrange(-1,2)
         y = fueldata[i][2] + randrange(-1,2)
         self.board[x][y] ^= FSTATION
         xx = BORDER + self.xunit * x + self.xunit//2
         yy = BORDER + self.yunit * y + self.yunit//2
         rr = STATIONSIZE
         id = self.can.create_rectangle(xx-rr,yy-rr,xx+rr,yy+rr,fill='red')
         self.stuff[(x,y)] = (id, FUEL, self.clock)

   def okrefill(self,x,y):
      s = self.stuff[(x,y)]
      if s[1] != 0:
         return False
      if (self.clock - s[2]) < REFILL:
         return False
      for i in range(NPLAYERS):
         if abs(x - self.player[i].x) + abs(y - self.player[i].y) < TOOCLOSE:
            return False
      return True

   def checkstations(self):
      global REFILL

      for (x,y) in self.stuff:
         s = self.stuff[(x,y)]
         if self.okrefill(x,y):
            self.stuff[(x,y)] = (s[0], FUEL, self.clock)
            self.can.itemconfigure(s[0], fill="red")
            self.board[x][y] ^= ESTATION
            self.board[x][y] ^= FSTATION
            REFILL += 50

   def setup(self):

      self.clock   = 0
      self.turn    = 0
      self.running = False

      self.board = []
      for i in range(self.cols):
         self.board.append([0 for j in range(self.rows)])     

      self.makestations()

      self.player = []
      for i in range(NPLAYER):
         self.player.append(Player(self,i,initposX[i],initposY[i]))

      self.robo = [None] * NPLAYER
      dims = (GAMEWID,GAMEHGT)
      for i in range(NPLAYER):
         pos = (initposX[i],initposY[i])
         self.robo[i] = RoboList[i](i, INITENERGY, pos, dims)
         self.namelab[i].configure(text=str(self.robo[i]))

      for i in range(self.rows):
         for j in range(self.cols):
            print("{0:4x}".format(self.board[j][i]),end='')
         print()

   def getemptysquare(self):
      while True:
         x = randrange(GAMEWID)
         y = randrange(GAMEHGT)
         if self.board[x][y] == 0:
            return (x,y)

   def getobstacle(self,x,y,dir):
      dx   = [ 1, 0,-1, 0]
      dy   = [ 0,-1, 0, 1]
      tx, ty = x, y
      n = 0
      while not self.wall[(tx,ty)][dir]:
         tx += dx[dir]
         ty += dy[dir]
         n += 1
         if self.board[tx][ty] != 0:
            return (n,self.board[tx][ty])
      return (n,WALL)

   def getprobe(self, x, y):
      vw = []
      for i in range(4):
         vw.append(self.getobstacle(x,y,i))
      return vw

   def getview(self, x, y, pno):
      dx   = [ 1, 0,-1, 0]
      dy   = [ 0,-1, 0, 1]
      vw = []
      for i in range(4):
         if self.wall[(x,y)][i]:
            vw.append(WALL)
         else:
            vw.append(self.board[x+dx[i]][y+dy[i]])
      vw.append(self.player[pno].energy)
      return vw

   def make_grid(self):
      for i in range(self.cols):
         x = BORDER+self.xunit*i
         for j in range(self.rows):
            y = BORDER+self.yunit*j
            if i > 0 and self.wall[(i,j)][2]:
               w = self.can.create_line(x, y-1, x, y+self.yunit+1, width=self.wallwidth)
            if j > 0 and self.wall[(i,j)][1]:
               w = self.can.create_line(x-1, y, x+self.xunit+1, y, width=self.wallwidth)
      self.can.create_rectangle(BORDER, BORDER, self.wid-BORDER, self.hgt-BORDER, width=1 + self.wallwidth)

   def cmdHandler(self,who):
      dx   = [1,0,-1,0]
      dy   = [0,-1,0,1]
      x = self.player[who].x
      y = self.player[who].y
      vw = self.getview(x,y,who)
      self.robo[who].feedback((FEEDBACK_VIEW,vw))
      cmd, dir = self.robo[who].action()
      if not self.player[who].update(-energyuse[cmd]):
         s = '{0:s} runs of out fuel'.format(str(self.robo[who]))
         self.info.configure(text=s)
         self.running = False
         return
      newx = x+dx[dir]
      newy = y+dy[dir]
      if cmd == CMD_SHOOT:
         if not self.wall[(x,y)][dir]:
            if isPlayer(self.board[newx][newy]):
               tar = getPlayerNumber(self.board[newx][newy])
               if tar < 0:
                  print('Major screwup in cmdHandler')
                  return
               de = self.player[tar].energy // 2
               s = '{0:s} shoots and takes {1:d} from {2:s}'.format(str(self.robo[who]),de,str(self.robo[tar]))
               self.info.configure(text = s)
               self.player[who].energy += de
               self.player[who].update(de)
               self.robo[who].feedback((FEEDBACK_HIT,tar))
               self.robo[who].feedback((FEEDBACK_FUEL,self.player[who].energy))
               self.player[tar].update(-de)
               rx, ry = self.getemptysquare()
               self.robo[tar].feedback((FEEDBACK_GOTHIT,(x,y)))
               self.robo[tar].feedback((FEEDBACK_FUEL,self.player[who].energy))
               self.player[tar].move(rx,ry)
            else:
               print('player', who, 'shoots into an empty room')
               self.robo[who].feedback((FEEDBACK_MISS,tar))
         else:
            print('player', who, 'shoots into an empty room')
            self.robo[who].feedback((FEEDBACK_MISS,tar))
      elif cmd == CMD_PROBE:
         vw = self.getprobe(x,y)
         self.robo[who].feedback((FEEDBACK_PROBE,vw))
      elif cmd == CMD_MOVE:
         if not self.wall[(x,y)][dir]:
            if (newx,newy) in self.stuff:
               (id,val,_) = self.stuff[(newx,newy)]
               self.player[who].energy += val
               self.scorelab[who].configure(text=str(self.player[who].energy))
               self.can.itemconfigure(id,fill="pink")
               self.stuff[(newx,newy)] = (id, 0, self.clock) 
               if isFullStation(self.board[newx][newy]):
                  self.board[newx][newy] ^= ESTATION
                  self.board[newx][newy] ^= FSTATION
            self.player[who].move(newx, newy)
      elif cmd == CMD_REST:
         pass
      else:
         print('whoops from', self.player[who],': command =', cmd)

   def playgame(self):
      self.cmdHandler(self.turn)
      self.turn = (self.turn + 1) % NPLAYER
      self.clock += 1
      if self.clock % 10 == 0:
         self.checkstations()
      if self.running:
         self.win.after(self.ticker.get(),self.playgame)
         
   def automate(self):
      if self.running:
         return
      self.running = True
      self.win.after(self.ticker.get(),self.playgame)

   def stop(self):
      self.running = False

def reset():
  win = Tk()
  win.geometry("+500+10")
  game = Game(win,GAMEHGT,GAMEWID)
  win.mainloop()

if __name__ == '__main__':
   
   reset()

