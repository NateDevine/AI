#!/usr/bin/env python3

#
# player 1 is b and wants the board value large
# player 2 is r and wants the board value small
#

from winners import winlist
import random
import sys

WIDTH = 7
BSIZE = 42

def save(board, val):
  fd = open('save.hash','a')
  fd.write("{0:s}:{1:d}\n".format(board,val))
  fd.close()
  #print("added new board not seen before to save.hash")

def boardeval1(board, who):
  val=0
  fd = open('save.hash','r')
  boardstr=''
  
  
  for i in board:
    boardstr+=str(i)
    
  for line in fd.readlines():
    s = line.strip()
    a = s.split(':')
    if boardstr==a[0]:
      if int(a[1])!=0:
        return int(a[1])
      
  for i in winlist:
    b=0
    r=0
    for j in range(0,4):
      if int(board[i[j]])==2:
        r+=1
      elif int(board[i[j]])==1:
        b+=1
    
    val+=(2**(3*b)-(2**(3*r)))
    
    if b==4: 
      val=5000
      break
    elif r==4:
      val=-5000
      break
    
    
  save(boardstr,val)
  
  fd.close()
  return val
  


def boardeval(board,who):
    
  newboard=board.copy()
  val=boardeval1(newboard,who)

  return val

class Player:
  
  rv = [0.5, 1.0, 0.0]

  def __init__(self,whoami):

    self.newgame()

  def newgame(self):

    self.prev = None
    

  def getmove(self,board,who):
    
    #fd = open('save.hash\n','w')
    #fd.write("starting new")
    #fd.close()
    
    #print("all boards it considered, and their value are now in save.hash")
    
    return boardeval(board,who)
 
 
  def __str__(self):
    return 'Nate Devine CS47503'

  def gameover(self,board,who):
    pass

  def datadump(self):
    pass
 
if __name__ == "__main__":

  boardstr=sys.argv[1]
  
  board=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  j=0
  
  for i in boardstr:
    board[j]=i
    j+=1
    
  print("Board value is: ",boardeval(board,1))
  

