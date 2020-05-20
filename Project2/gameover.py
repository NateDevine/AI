#!/usr/bin/env python3

#
# player 1 is b and wants the board value large
# player 2 is r and wants the board value small
#

from winners import winlist
import random
import sys


def gameover(board):
  w=0
  for i in winlist:
    b=0
    r=0
    for j in range(0,4):
      
      if int(board[i[j]])==2:
        r+=1
      elif int(board[i[j]])==1:
        b+=1
      else: w+=1 
    if b==4: 
      return 1
    elif r==4:
      return 2
 
  
  if not w: return 0
  else: return 3
 
if __name__ == "__main__":

  boardstr=sys.argv[1]
    
  print(gameover(boardstr))
  

