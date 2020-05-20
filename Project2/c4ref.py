#!/usr/bin/env python3

import sys
from winners import haswinner,winlist

#from player import Player as P2
from player03 import Player as P1
from player03 import Player as P2

BSIZE = 42
WIDTH = 7

class C4Referee:

    def __init__(self):

        self.plyr1 = P1(1)
        self.plyr2 = P2(2)
        self.gameover = False
        self.reset()

    def reset(self):
        
       if self.gameover:
           self.plyr1.gameover(self.board, self.winner)
           self.plyr2.gameover(self.board, self.winner)
       self.board = [0]*BSIZE
       self.stack = [i for i in range(WIDTH)]
       self.gameover = False
       self.movecount = 0
       self.winner = 0

    def player1move(self):
        #print("start p1 move")
        k = self.plyr1.getmove(self.board, 1)
        if k < 0:
            self.gameover = True
            return
        m = self.stack[k]
        self.stack[k] += WIDTH
        self.board[m%42] = 1
        self.movecount += 1

    def player2move(self):
        #print("start p2 move")
        k = self.plyr2.getmove(self.board, 2)
        if k < 0:
            self.gameover = True
            return
        m = self.stack[k]
        self.stack[k] += WIDTH
        self.board[m%42] = 2
        self.movecount += 1

    def runner(self, ngames = 100):

        tally = [0,0,0]
        n = 0
        while n < ngames:
           if self.gameover:
               n += 1
               self.reset()
           self.player1move()
           if haswinner(self.board,1):
               self.winner = 1
               tally[1] += 1
               self.gameover = True
               continue
           elif self.movecount == BSIZE:
               self.winner = 0
               tally[0] += 1
               self.gameover = True
               continue
           self.player2move()
           if haswinner(self.board,2):
               self.winner = 2
               tally[2] += 1
               self.gameover = True
           elif self.movecount == BSIZE:
               self.winner = 0
               tally[0] += 1
               self.gameover = True
        print(tally)
        self.plyr1.datadump()
        self.plyr2.datadump()

if __name__ == "__main__":

   if len(sys.argv) > 1:
      n = int(sys.argv[1])
   else:
      n = 100
   game = C4Referee()
   game.runner(n)

