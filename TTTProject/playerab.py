
NOTDONE = 99
BSIZE = 9

count = 0

winners = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))

class Player03:

   def __init__(self, who):
      self.who = who if who == 1 else -1

   def boardvalue(self,board,who):
      for win in winners:
         if all([board[x] == who for x in win]):
            return who
      if not 0 in board:
         return 0
      return NOTDONE

   def alphabeta(self,depth,board,who):
      global count

# player X wants the value of the board to be large
# player O wants the value of the board to be small
# start them with some value they can beat

      count += 1

      best = -2 if (who == 1) else 2
      movelist = [x for x in range(BSIZE) if board[x] == 0]
      bestmove = movelist[0]
      for mov in movelist:
         board[mov] = who
         val = self.boardvalue(board,who)
         if val == NOTDONE:
            val = self.alphabeta(depth+1, board, -who)
         if val*who > best*who:
            best, bestmove = val, mov
         board[mov] = 0
      return bestmove if (depth == 0) else best

   def getmove(self, oldboard):
      global count
#
# On first move, use center if empty, otherwise use lower right corner.
# Note that 'sum' does what one would hope on a list of boolean values.
#
#   This makes things much faster, since the first move is where the alpha/beta
#   pruner spends most of it's time.
#
      if sum([x != 0 for x in oldboard]) < 2:
        return 4 if oldboard[4] == 0 else 8

# changing the 2's to -1's on the board I get from the referee

      newboard =  [(-1 if (x == 2) else x) for x in oldboard]
      count = 0
      mov = self.alphabeta(0, newboard, self.who)
      #print(count)
      return mov

   def gameover(self,board,who):
      pass

   def datadump(self):
      pass
