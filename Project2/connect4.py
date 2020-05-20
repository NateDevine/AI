#!/usr/bin/env python3

import sys
from getmove import getmove
from printboard import printboard
from gameover import gameover
from winners import haswinner,winlist


def humMove(board, who):
  c=[(35,28,21,14,7,0),
     (36,29,22,15,8,1),
     (37,30,23,16,9,2),
     (38,31,24,17,10,3),
     (39,32,25,18,11,4),
     (40,33,26,19,12,5),
     (41,34,27,20,13,6)]
  m=[35,36,37,38,39,40,41]
  for i in range(0,7):
    for j in range(0,6):
      if(board[c[i][j]]=='0'):
        m[i]=c[i][j]
  move=int(input("your move: "))
    
  j=0
  bl=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  for i in board:
    bl[j]=i
    j+=1
  
  bl[m[move]]=who
  b=''
  for i in bl: b+=str(i)
  
  return b
  
def compMove(board, who):
  move=getmove(board, who)
  
  c=[(35,28,21,14,7,0),
     (36,29,22,15,8,1),
     (37,30,23,16,9,2),
     (38,31,24,17,10,3),
     (39,32,25,18,11,4),
     (40,33,26,19,12,5),
     (41,34,27,20,13,6)]
  m=[35,36,37,38,39,40,41]
  for i in range(0,7):
    for j in range(0,6):
      if(board[c[i][j]]=='0'):
        m[i]=c[i][j]
  
  j=0
  bl=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  for i in board:
    bl[j]=i
    j+=1
  
  #print(m[move])
  bl[m[move]]=who
  b=''
  for i in bl: b+=str(i)
  
  return b


if __name__=="__main__":
  board="000000000000000000000000000000000000000000"
  
  i=1
  while(gameover(board)==3):
    
    if i == 1:
      board=compMove(board,i)
      i=2
      continue
    elif i==2:
      printboard(board)
      print(' ')
      board=humMove(board,i)
      i=1
      continue
    else: print("this should never happen")
    
  printboard(board)
  