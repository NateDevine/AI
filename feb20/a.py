#!/usr/bin/env python3
  
import sys
import random as rnd
from tkinter import *
from makemoves import makemovelist

WIDTH  = 1200
HEIGHT =  900
VBASE  =  100
HWIDTH = WIDTH // 2

RAD =  24
WID = 100
HGT = 160

vlist = [[ 0, 0],
         [-1, 1], [ 1, 1],
         [-2, 2], [ 0, 2], [ 2, 2],
         [-3, 3], [-1, 3], [ 1, 3], [ 3, 3],
         [-4, 4], [-2, 4], [ 0, 4], [ 2, 4], [ 4, 4]]

elist = [[1,2], [2,3,4], [4,5], [4,6,7], [5,7,8], [8,9],
         [7,10,11], [8,11,12], [9,12,13], [13,14],
         [11], [12], [13], [14], []]

colorlist = ['gray','red']

class Game(Tk):

   def __init__(self):
      Tk.__init__(self)
      self.title("Cracker Barrel")
      self.can = Canvas(self, width=WIDTH, height=HEIGHT, bg='gray')
      self.can.pack()

      self.option_add("*font",("Helvetica",36))
      self.quit = Button(self,text='Quit',height=1,relief=RAISED,fg="#000",bg="dodgerblue",command=self.destroy)
      self.quit.pack(side=LEFT,fill=X)
      self.play = Button(self,text='Play',height=1,relief=RAISED,fg="#000",bg="dodgerblue",command=self.click)
      self.play.pack(side=RIGHT,fill=X)

      self.movelist = makemovelist()
      self.reset()
      self.drawboard()

   def reset(self):
      self.gameover  = False
      self.nmoves    = 0
      self.state     = [False] + [True]*14

   def drawboard(self):
      for i in range(15):
         x1 = WID * vlist[i][0] + HWIDTH
         y1 = HGT * vlist[i][1] + VBASE
         for j in elist[i]:
            x2 = WID * vlist[j][0] + HWIDTH 
            y2 = HGT * vlist[j][1] + VBASE
            self.can.create_line(x1, y1, x2, y2, fill='black', width = 4)
      for i in range(15):
         x = WID * vlist[i][0] + HWIDTH
         y = HGT * vlist[i][1] + VBASE
         c = colorlist[self.state[i]]
         self.can.create_oval(x - RAD, y - RAD, x + RAD, y + RAD, outline='black', fill=c, width = 4)
 
   def checkmove(self,n):
      b = self.movelist[n]
      if self.state[b[0]] and self.state[b[1]] and not self.state[b[2]]:
         return True
      return False
 
   def makemove(self,n):
      if self.checkmove(n):
         b = self.movelist[n]
         self.state[b[0]] = False
         self.state[b[1]] = False
         self.state[b[2]] = True
         return True
      return False

   def click(self):
      if self.gameover:
         self.reset()
         self.drawboard()
         return
      ml = list(range(len(self.movelist)))
      rnd.shuffle(ml)
      for i in ml:
         if self.makemove(i):
            self.nmoves += 1
            self.drawboard()
            return
      self.gameover = True
      print(self.nmoves)

if __name__ == '__main__':

   game = Game()
   game.mainloop()

