#!/usr/bin/env python3

#
# player 1 is X and wants the board value large
# player 2 is O and wants the board value small
#
# Note: this version simply returns a random move
#

import random
import sys

WIDTH = 7
BSIZE = 42

class Player:

  rv = [0.5, 1.0, 0.0]

  def __init__(self,whoami):

    self.newgame()

  def newgame(self):

    self.prev = None

  def getmove(self,board,who):

    stack = list(range(WIDTH))
    for i in range(WIDTH):
      while stack[i] < BSIZE and board[stack[i]] != 0:
        stack[i] += WIDTH

# possible infinite loop

    while True:
      x = random.randrange(0,7)
      if stack[x] < BSIZE:
        return x
 
  def __str__(self):
    return 'Random Player'

  def gameover(self,board,who):
    pass

  def datadump(self):
    pass
 
if __name__ == "__main__":

  pass

