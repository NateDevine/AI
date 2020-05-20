
from random import choice

winList =((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6))

class Player03:

   def __init__(self, who):
      self.who = who  

   def __str__(self):
      return("Nate Devine")
    
   def gameover(self,board,who):
      pass

   def getmove(self,board):
      if not 0 in board:
         return -1
       
      for i in range(0,8):
         if board[winList[i][0]]==board[winList[i][1]] and board[winList[i][0]]!=0 and board[winList[i][2]]==0: 
	    #first checking for 2 in a row, then making sure it isnt seeing 2 blank spaces in a row, and finally making sure it can move there before returning
            return winList[i][2]
         if board[winList[i][1]]==board[winList[i][2]] and board[winList[i][1]]!=0 and board[winList[i][0]]==0:
            #first checking for 2 in a row, then making sure it isnt seeing 2 blank spaces in a row, and finally making sure it can move there before returning
            return winList[i][0]
         if board[winList[i][0]]==board[winList[i][2]] and board[winList[i][0]]!=0 and board[winList[i][1]]==0:
	    #first checking for 2 in a row, then making sure it isnt seeing 2 blank spaces in a row, and finally making sure it can move there before returning
            return winList[i][1]

      return choice([x for x in range(9) if board[x] == 0])

