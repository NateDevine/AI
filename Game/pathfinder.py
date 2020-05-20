#!/usr/bin/env python3

#
# finds shortest paths for map in Game format
# each vertex is an (x,y) tuple. the tuples
# are dictionary keys.  the dictionary values
# True/False lists for each direction.  True
# indicates there is a wall, False indicates
# the is no (known) wall.
#

from heapq import heappush, heappop
from makemaze import Maze                      # used only when main is run.

SIZE = 5                                       # used only when main is run.

dx   = [1, 0,-1, 0]
dy   = [0,-1, 0, 1]

#
# walls is a ddictionary of lists of four True/False value
#
# start is a tuple = (x,y) of start of path
# finish is a tuple = (x,y) of the end of the path
#

def dijkstra(walls,start,finish):
   global dx, dy

   xstart, ystart = start
   xfinish, yfinish = finish
   vlist = []
   for key in walls:
      vlist.append(key)

   u = (xstart,ystart)
   w = (xfinish, yfinish)
   pq = [(0,u,())]
   visited = set()
   mindist = {u : 0}
   while pq:
      (dist,u,path) = heappop(pq)
      if u not in visited:
         visited.add(u)
         path = (*path, u)
         if u == w:
            return path
         for i in range(4):
            if walls[u][i]:
               continue
            v = (u[0] + dx[i], u[1] + dy[i])
            if v in visited:
               continue
            pdist = mindist.get(v, None)
            ndist = dist + 1
            if pdist == None or ndist < pdist:
               mindist[v] = ndist
               heappush(pq,(ndist,v,path))
   print('no path from',start,'to',finish)
   return []
      
if __name__ == "__main__":

   maze = Maze(SIZE,SIZE)
   walls = maze.getwalls()

   path = dijkstra(walls, (0,0), (SIZE-1,SIZE-1))
   for v in path:
      print(v)

