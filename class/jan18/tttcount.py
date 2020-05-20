#!/usr/bin/env python3

BSIZE = 9

count = 0

winnerlist = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))

def game_not_over(board, who):
   for win in winnerlist:
      if all([board[x] == who for x in win]):
         return False
   if 0 in board:
      return True
   return False

def recurse(board, who):  # who = 1 or 2
   global htab, count

   movelist = [x for x in range(BSIZE) if board[x] == 0]
   for m in movelist:
      board[m] = who
      key = str(board)
      if key not in htab:
         count += 1
         htab[key] = True
         if game_not_over(board,who):
            recurse(board, 3 - who)     # hack
      board[m] = 0

if __name__ == "__main__":

   board = [0]*BSIZE
   key = str(board)
   htab = {key : True}
   recurse(board, 1)   # players are 1 and 2
   print(len(htab))

