#!/usr/bin/env python3

import tkinter as tk

BSIZE = 9

symbol = (' ', 'X', 'O')

winners = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))

class Board:

   def __init__(self, win):
 
      self.turn = 1
      self.gameover = False
      self.board = [0]*BSIZE

      win.option_add("*font",("Helvetica",32))
      self.lablist = []
      for i in range(BSIZE):
         lab = tk.Label(win, text='', relief = tk.RAISED, width = 5, height = 3)
         lab.grid(row = i // 3, column = i % 3)
         lab.bind('<Button-1>', self.callback)
         lab.pos = i
         self.lablist.append(lab)

   def reset(self):
      self.turn = 1
      self.gameover = False
      self.board = [0]*BSIZE
      for lab in self.lablist:
         lab.configure(text='')

   def callback(self, event):
      if self.gameover:
         self.reset()
         return
      pos = event.widget.pos
      if self.board[pos] != 0:
         return
      self.board[pos] = self.turn
      print(self.board)
      event.widget.configure(text=symbol[self.turn])
      val = self.boardvalue(self.turn)
      if val == self.turn:
         print(symbol[self.turn],'wins')
         self.gameover = True
         return
      elif val == 0:
         print('tie game')
         self.gameover = True
         return
      self.turn = 3 - self.turn

   def boardvalue(self,who):
      for win in winners:
         if all([self.board[x] == who for x in win]):
            return who
      if not 0 in self.board:    # tie game
         return 0
      return 99                  # game not over

if __name__ == "__main__":

   win = tk.Tk()
   game = Board(win)
   win.mainloop()

