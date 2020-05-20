
from random import choice


class Player03:

   def __init__(self, who):
      self.who = who  

   

   def getmove(self,board):
      if not 0 in board:
         return -1
       
      return choice([x for x in range(9) if board[x] == 0])

