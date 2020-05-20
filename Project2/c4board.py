#!/usr/bin/env python3

from tkinter import *
from winners import haswinner,winlist
import player03 as player

colorlist = ["#111","#c22","#22c"]

BSIZE = 42
WIDTH = 7

class C4Board:

    def __init__(self,win,fname=None):

        self.human = 2
        self.computer = 1

        self.board = [0]*BSIZE
        self.stack = [i for i in range(WIDTH)]
        self.plyr = player.Player(self.computer)
        self.gameover = False
        self.movecount = 0

        if fname:
            self.plyr.restore(fname)

        win.option_add("*font",("Helvetica",24))
        win.title("Connect-4")

        boardframe = Frame(win)
        boardframe.pack(side='top')
        self.boardframe = boardframe

        flist = []                                            # six frames in the connect-4 board
        for i in range(WIDTH):                            # each frame is a column of six buttons (actually labels)
            flist.append(LabelFrame(boardframe))
            flist[i].pack(side='left')
        self.framelist = flist                    # framelist is the list of frames

        lab = Label(win,bg="#222",fg="#f0f")        # feedback label -- shows who won
        lab.pack(side='bottom',fill=BOTH)
        self.lab = lab

        blist = []
        for i in range(BSIZE):
            but = Label(flist[i % WIDTH],text=str(i),width=5,height=2,relief=RAISED,bg=colorlist[0],fg="#ff0")
            but.pos = i % WIDTH
            but.state = 0
            but.pack(side="bottom")
            but.bind("<Button-1>", self.callback)
            blist.append(but)
        self.buttonlist = blist            # buttonlist is the list of BSIZE buttons, one per square

        self.reset()

    def reset(self):
        self.board = [0]*BSIZE
        self.stack = [i for i in range(WIDTH)]
        self.gameover = False
        self.movecount = 0
        for i in range(BSIZE):
            self.buttonlist[i].configure(bg=colorlist[0])
            self.buttonlist[i].state = 0
        self.lab.configure(text='')
        if self.computer == 1:
            self.computermove()

    def computermove(self):
        board=""
  
        for i in self.board:
          board+=str(i)
  
        #print(board)
        k = self.plyr.getmove(self.board, 1)
        if k < 0:
            self.gameover = True
            return
        m = self.stack[k]
        if m>=42: return
        self.stack[k] += WIDTH
        self.buttonlist[m].configure(bg=colorlist[2])
        self.buttonlist[m].state = 2
        self.board[m] = self.computer
        self.movecount += 1
        
        

    def humanmove(self,event):
        board=""
  
        for i in self.board:
          board+=str(i)
          
        #print(board)
        k = event.widget.pos
        if self.stack[k] >= BSIZE:
            return
        m = self.stack[k]
        self.stack[k] += WIDTH
        self.buttonlist[m].configure(bg=colorlist[1])
        self.buttonlist[m].state = 1
        self.board[m] = self.human
        self.movecount += 1
        

    def callback(self,event):

        if self.gameover:
            self.reset()
            return
        self.humanmove(event)
        if haswinner(self.board,self.human):
            self.lab.configure(text='Human wins.')
            self.gameover = True
            return
        elif self.movecount == BSIZE:
            self.lab.configure(text='Tie game.')
            self.gameover = True
            return
        self.computermove()
        if haswinner(self.board,self.computer):
            self.lab.configure(text='Computer wins.')
            self.gameover = True
            return
        elif self.movecount == BSIZE:
            self.lab.configure(text='Tie game.')
            self.gameover = True
            return
        
#
# first part responds to mouse click to make the user's move
#
        if self.gameover:
            self.reset()
            return

if __name__ == "__main__":

    win = Tk()
    game = C4Board(win)
    win.mainloop()

