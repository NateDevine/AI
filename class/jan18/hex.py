#!/usr/bin/env python3
  
import sys
from tkinter import *
from math import sin,cos,sqrt,radians

colorlist = ['#f5deb3', '#2010d0', '#d01020', '#777777']

class Graph:                                       

   def __init__(self,n):
      self.n = n
      self.nedges = 0
      self.initcolor()
      self.alist = [[] for _ in range(n)]

   def __str__(self):
      s = '{} vertices and {} edges\n'.format(self.n,self.nedges)
      for u in range(self.n):
         t = '{0:2d}:'.format(u)
         s += t
         for v in self.alist[u]:
            t = '{0:4d}'.format(v)
            s += t
         s += '\n'
      return s

   def addedge(self,u,v):
      if u in self.alist[v]:
         return
      if v in self.alist[u]:
         sys.stderr.write('addedge error: {},{}\n'.format(u,v))
         return
      self.alist[v].append(u)
      self.alist[u].append(v)
      self.nedges += 1

   def dfs(self,u,c):
      self.scanned[u] = True
      for v in self.alist[u]:
         if self.clist[v] == c and not self.visited[v]:
            self.visited[v] = True
            self.toscan.append(v)
      if len(self.toscan) > 0:
        v = self.toscan.pop(0)
        self.dfs(v, c)

   def areconnected(self,u,v):
      self.toscan = []
      self.scanned = [False] * self.n
      self.visited = [False] * self.n
      self.visited[u] = True
      self.dfs(u, self.clist[u])
      return self.visited[v]

   def initcolor(self):
      n = self.n
      self.clist = [0]*n
      self.clist[n-4] = self.clist[n-1] = 1
      self.clist[n-3] = self.clist[n-2] = 2

class Hexagon:
   
   hexcount = 0

   def __init__(self, parent, x, y, sidelen, color):
      self.parent = parent
      self.x = x
      self.y = y
      self.sidelen = sidelen
      self.color = color             # color number
      xlist = []
      ylist = []
      for theta in range(0,360,60):
         hx = x + sidelen * cos(radians(theta))
         hy = y + sidelen * sin(radians(theta))
         xlist.append(hx)
         ylist.append(hy)
      k = self.parent.create_polygon(xlist[0],ylist[0], xlist[1],ylist[1], xlist[2],ylist[2],
                                     xlist[3],ylist[3], xlist[4],ylist[4], xlist[5],ylist[5], 
                                     fill=colorlist[self.color], width=2.0,
                                     outline="black", tags=Hexagon.hexcount)
      self.itemno = k
      Hexagon.hexcount += 1

   def recolor(self,c):
      self.parent.itemconfigure(self.itemno,fill=colorlist[c])
      self.color = c
      
class HexGrid(Tk):

   def __init__(self):
      Tk.__init__(self)
      self.title("Hex")
      self.can = Canvas(self, width=1000, height=750, bg=colorlist[0])
      self.can.pack()

      self.gameover = False
      self.turn = 1

      self.hexagons = []
      self.make_grid(4, 60, debug=True)
      self.make_graph()
      self.option_add("*font",("Helvetica",36))
      self.lab = Label(self,text='Play',height=1,relief=RAISED,fg="#000",bg=colorlist[0])
      self.lab.pack(fill=BOTH)
      self.can.bind("<Button-1>", self.click)
      
   def make_grid(self, dim, side, debug):
      alpha = [0, 0, 0, 0, 1, 2, 3]
      omega = [1, 2, 3, 4, 4, 4, 4]
      xborder = 225
      yborder = 350
      x0 = xborder + 4.5*side
      y0 = yborder
      x1 = xborder - 1.5*side
      x2 = xborder + 10.5*side
      y1 = yborder + 3*sqrt(3)*side
      y2 = yborder - 3*sqrt(3)*side
      self.can.create_polygon(x0,y0,x0,y1,x1,y1,x1,y0, fill=colorlist[2], width=2.0, outline="black")
      self.can.create_polygon(x0,y0,x0,y2,x1,y2,x1,y0, fill=colorlist[1], width=2.0, outline="black")
      self.can.create_polygon(x0,y0,x0,y1,x2,y1,x2,y0, fill=colorlist[1], width=2.0, outline="black")
      self.can.create_polygon(x0,y0,x0,y2,x2,y2,x2,y0, fill=colorlist[2], width=2.0, outline="black")
      for a in range(7):
         b1 = alpha[a]
         b2 = omega[a]
         for b in range(b1,b2):
            x = xborder + 1.5 * a * side
            y = yborder + sqrt(3) * side * (b - a / 2)
            print('{0:2d} {1:2d} {2:9.3f} {3:9.3f}'.format(a,b,x,y))
            h = Hexagon(self.can, x, y, side, 3)
            h.a = a
            h.b = b
            self.hexagons.append(h)

   def reset(self):
      for h in self.hexagons:
         h.recolor(3)
      self.graph.initcolor()
      self.turn = 1
      self.gameover = False
      self.lab.configure(text='Play again')

   def make_graph(self):
      r1list = [0,1,3,6]
      b1list = [6,10,13,15]
      b2list = [0,2,5,9]
      r2list = [9,12,14,15]

      n = len(self.hexagons)
      self.graph = Graph(n+4)
      m = 0
      for i in range(n-1):
         u = self.hexagons[i]
         for j in range(i+1,n):
            v = self.hexagons[j]
            if u.a + 1 == v.a:
               if v.b - u.b in [0,1]:
                  self.graph.addedge(i,j)
            elif u.a == v.a:
               if u.b + 1 == v.b:
                  self.graph.addedge(i,j)
      for v in r1list:
         self.graph.addedge(n,v)
      for v in b1list:
         self.graph.addedge(n+1,v)
      for v in b2list:
         self.graph.addedge(n+2,v)
      for v in r2list:
         self.graph.addedge(n+3,v)
      print(self.graph)

   def click(self, ev):
      if self.gameover:
         self.reset()
         return
      clicked = self.can.find_closest(ev.x, ev.y)[0]
      if clicked < 5:
         return
      v = int(self.can.gettags(clicked)[0])
      c = self.hexagons[v].color
      if c != 3:
         return
      self.graph.clist[v] = self.turn
      self.hexagons[v].color = self.turn
      self.can.itemconfigure(clicked, fill=colorlist[self.turn])
      print(self.graph)

# computer moves:

      n = self.graph.n
      if self.turn == 1:
         if self.graph.areconnected(n-1,n-4):
            self.lab.configure(text='Blue wins')
            self.gameover = True
      elif self.turn == 2:
         if self.graph.areconnected(n-2,n-3):
            self.lab.configure(text='Red wins')
            self.gameover = True
      self.turn = 3 - self.turn

if __name__ == '__main__':

   game = HexGrid()
   game.mainloop()

