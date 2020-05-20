#!/usr/bin/env python3

import tkinter as tk

#
# Tic Tac Toe - Computer plays 'O' using alpha-beta pruning
#   
#   players are 1 and -1
#


# gameover returns the number of the winner, if there is a winner.
# otherwise it returns 0 if the game is finished (board full) or
# returns 2 if the game is not finished
#

def gameover(board):
   global wins

   for pat in wins:
      w = board[pat[0]]
      if w != 0:
         if board[pat[1]] == w and board[pat[2]] == w:
            return w
   if 0 in board:
      return 2
   return 0

#
# the computer finds its best move by looking at all possible continuations
#
# using +1 and -1 for the players makes it easy to combine the two cases
#

def alphabeta(depth, who, board):
   li = [x for x in range(len(board)) if board[x] == 0]     # make a list of valid moves
   max = -2 * who                                           # start max at something we will beat
   for x in li:                    # for each move
      board[x] = who                 # make the move
      t = gameover(board)            # evaluate the resulting board
      if t == 2:                     # if the game isn't over, get the value by recursing
         t = alphabeta(depth+1,-who,board)
      if who * t > who * max:        # when who == -1 the inequality is reversed
         max, mov = t,x
      board[x] = 0                   # unmake the move
   if depth == 0:                    # at level 0 return the move
      return mov
   else:
      return max                     # otherwise return the value of the move

#
# almost everything else deals with graphics
#

def callback(event):
   global butlist, board, lab, done

   if done:                             # is the game over?
      return
   w = event.widget                     # get the widget that was clicked
   if w.used:                           # if that square is already filled, ignore click
      return
   w.used = True                        # mark the graphical board
   w.configure(text="X")                # place an X there (the human)
   k = event.widget.pos                 # get the board number for the widget clicked
   board[k] = 1                         # mark the logical board (the list of 9 integers)
   k = gameover(board)                  # check to see if the move ends the game
   if k == 1:                           # the human won (this won't happen!)
      lab.configure(text="You win.")
      done = True
      return
   elif k == 0:                         # it was a tie (this will happen)
      lab.configure(text="Tie.")
      done = True
      return

   k = alphabeta(0,-1,board)            # otherwise game is not over, so the computer moves
   lab.configure(text="")
   board[k] = -1                        # mark the boards (graphical and logical) as above
   butlist[k].used = True
   butlist[k].configure(text="O")
   k = gameover(board)
   if k == -1:
      lab.configure(text="You lose.")
      done = True
      return

if __name__ == "__main__":

   wins = [[0,1,2],[3,4,5],[6,7,8],
           [0,3,6],[1,4,7],[2,5,8],
           [0,4,8],[2,4,6]]

   board = [0]*9

   colorlist = ["#111","#333"]
   done = False

   root = tk.Tk()
   root.option_add("*font",("Helvetica",32))
   root.title("Tic Tac Toe")

   framelist = [0]*3
   for i in range(3):
      framelist[i] = tk.Frame(root)
      framelist[i].pack()

   lab = tk.Label(root,bg="#222",fg="#f0f")
   lab.pack(fill=tk.BOTH)

   butlist = []
   for i in range(9):
      but = tk.Label(framelist[i//3],text="",width=5,height=3,relief=tk.RAISED,bg=colorlist[i%2],fg="#ff0")
      but.pos = i
      but.used = False
      but.pack(side="left")
      but.bind("<Button-1>", callback)
      butlist.append(but)

   root.mainloop()

