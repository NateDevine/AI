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
  print("added new board not seen before to save.hash")

def boardeval1(board,m, who):
  val=0
  if(m!=100):  board[m]=who
  fd = open('save.hash','r')
  boardstr=''
  
  
  for i in board:
    boardstr+=str(i)
    
  for line in fd.readlines():
    s = line.strip()
    a = s.split(':')
    if boardstr==a[0]:
      return int(a[1])
      
  for i in winlist:
    b=0
    r=0
    for j in range(0,4):
      if int(board[i[j]])==2:
        r+=1
      elif int(board[i[j]])==1:
        b+=1     
    
    val+=(2**(2*b)-(2**(2*r)))
    
    if b==4: 
      val=5000
      break
    elif r==4:
      val=-5000
      break
    
    
  save(boardstr,val)
  
  fd.close()
  return val
  


def boardeval(boardstr,who):
  who=int(who)
  c=[(35,28,21,14,7,0), (36,29,22,15,8,1), (37,30,23,16,9,2), (38,31,24,17,10,3), (39,32,25,18,11,4), (40,33,26,19,12,5), (41,34,27,20,13,6)] #columns
    
  m=[35,36,37,38,39,40,41]  


  j=0
  board=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  for i in boardstr:
    board[j]=int(i)
    j+=1
    
    
  for i in range(0,WIDTH):
    f=0
    for j in range(0,6):
      if((int(board[c[i][j]])==0)):
        m[i]=c[i][j]
      else: 
        f+=1
    if f==6: 
      m[i]=100

  best=boardeval1(board,100,who)
  index=0
    
  for i in range(0,7):
    newboard=board.copy()
    if m[i]==100: continue
    val=boardeval1(newboard,m[i],who)
    if (val>best or val==-5000) and who==1:
      best=val
      index=i
      if best==5000 or best ==-5000: break
    elif (val<best or val==5000) and who==2:
      best=val
      index=i
      if best==5000 or best ==-5000: break
  return index

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
    
  print(boardeval(board,1))
  

