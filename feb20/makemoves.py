#!/usr/bin/env python3

seeds = [
   [ 0,  1,  3], [ 1,  3,  6], [ 3,  6, 10],
   [ 2,  4,  7], [ 4,  7, 11], [ 5,  8, 12],
   [ 0,  2,  5], [ 2,  5,  9], [ 5,  9, 14],
   [ 1,  4,  8], [ 4,  8, 13], [ 3,  7, 12],
   [ 3,  4,  5], [ 6,  7,  8], [ 7,  8,  9],
   [10, 11, 12], [11, 12, 13], [12, 13, 14]
]

def makemovelist():
   mklist = []
   for s in seeds:
      mklist.append(s)
      t = [*s]
      t.reverse()
      mklist.append(t)
   return mklist

if __name__ == "__main__":    

   mlist = makemovelist()
   for x in mlist:
      print(x)

