#!/usr/bin/env python3
  
import sys
import random as rnd
from tkinter import *
from makemoves import makemovelist

ALPHA  = 0.1

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

def stringify(li):
   return "".join([str(x) for x in li])

class Game(Tk):

   def __init__(self):
      Tk.__init__(self)
      self.title("Cracker Barrel")
      self.can = Canvas(self, width=WIDTH, height=HEIGHT, bg='gray')
      self.can.pack()

      self.option_add("*font",("Helvetica",36))
      self.quit = Button(self,text='Quit',height=1,relief=RAISED,fg="#000",bg="dodgerblue",command=self.destroy)
      self.quit.pack(side=LEFT,fill=X)
      self.save = Button(self,text='Save',height=1,relief=RAISED,fg="#000",bg="dodgerblue",command=self.save)
      self.save.pack(side=LEFT,fill=X)
      self.play = Button(self,text='Play',height=1,relief=RAISED,fg="#000",bg="dodgerblue",command=self.playone)
      self.play.pack(side=LEFT,fill=X)
      self.info = Label(self,text='0',width=12,relief=RAISED,fg="#000",bg="dodgerblue")
      self.info.pack(side=LEFT,fill=X)

      self.movelist = makemovelist()
      self.ngames = 0

      self.hashtab   = {}
      self.readhashtable()

      self.show = True
      self.reset()
      self.drawboard()

   def readhashtable(self):
      try:
         nr = 0
         fd = open('save.hash','r')
         for line in fd.readlines():
            s = line.strip()
            print(s)
            a = s.split(':')
            self.hashtab[a[0]] = float(a[1])
            nr += 1
         fd.close()
         print('read', nr, 'hashes')
      except:
         print('no hash table to read')

   def save(self):
      fd = open('save.hash','w')
      for k in self.hashtab:
         fd.write("{0:s}:{1:.9f}\n".format(k,self.hashtab[k]))
      fd.close()

   def reset(self):
      self.ngames += 1
      self.blist     = []
      self.gameover  = False
      self.nmoves    = 0
      self.state     = [0] + [1]*14

   def drawboard(self):
      if not self.show:
         return
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
         self.state[b[0]] = 0
         self.state[b[1]] = 0
         self.state[b[2]] = 1
         self.blist.append(stringify(self.state))
         return True
      return False
 
   def fakemove(self,n,bo):
       b = self.movelist[n]
       bo[b[0]] = 0
       bo[b[1]] = 0
       bo[b[2]] = 1
       return stringify(bo)

   def bestmove(self):
      mli = []
      vli = []
      for i in range(len(self.movelist)):
         if self.checkmove(i):
            mli.append(i)
            bo = [*self.state]
            k = self.fakemove(i,bo)
            if k in self.hashtab:
               vli.append(self.hashtab[k] + rnd.gauss(0,0.01))
            else:
               vli.append(0)
      if len(mli) == 0:
         return None
      print(mli)
      print(vli)
      m = mli[ max( list(range(len(mli))), key=lambda x: vli[x] ) ]
      return m

   def playone(self):
      if self.gameover:
         self.reset()
         self.drawboard()
         return
      m = self.bestmove()
      if m != None and self.makemove(m):
         self.nmoves += 1
         self.drawboard()
      else:
         self.gameover = True
         score = self.nmoves
         if score == 13 and self.state[0] == 1:
            score += 1
         self.info.configure(text = str(score))

if __name__ == '__main__':

   game = Game()
   game.mainloop()

