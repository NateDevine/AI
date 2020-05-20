import sys

def printboard(board):
  rows=[(35,36,37,38,39,40,41),
        (28,29,30,31,32,33,34),
        (21,22,23,24,25,26,27),
        (14,15,16,17,18,19,20),
        (7,8,9,10,11,12,13),
        (0,1,2,3,4,5,6)]
  
  print("     0 1 2 3 4 5 6\n")
  
  for row in rows:
    print("     ", end='')
    for i in range(0,7):
      print(board[row[i]], end=' ')
    print(" ")
      
if __name__=="__main__":
  
  printboard(sys.argv[1])