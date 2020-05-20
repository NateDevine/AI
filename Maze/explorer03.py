
from random import randrange, shuffle, choice

class Explorer:

   
   def seek(self, pos, goalpos):
     e=0
     n=1
     w=2
     s=3
     dmlist=([n,e,w,s],[s,e,n,w],[s,w,e,n],[n,w,e,s])
     
     newpos=[pos[0],pos[1]]
     
     self.seen.append(newpos)
     #print(self.seen)
     
     if pos[0]<=goalpos[0]:
       if pos[1]<=goalpos[1]: return dmlist[1]
       else: return dmlist[0]
     if pos[0]>=goalpos[0]:
       if pos[1]>=goalpos[1]: return dmlist[3]
       else: return dmlist[2]
   
   def __init__(self,xstart, ystart, xgoal, ygoal):
      self.lastmove = 0
      self.goalpos=[xgoal,ygoal]
      self.pos=[xstart,ystart]
      self.seen=[]
      self.dm = self.seek(self.pos, self.goalpos)
      
      
   def action(self):
      
      #print(self.dm)
      j=0
      for i in self.seen:
        if i==self.pos:
          m = 0
          while True: 
            m = randrange(4)
            if self.view[m] != 100:
              #print("random: ", m)
              self.lastmove = m
              if m==0: self.pos[0]+=1
              if m==1: self.pos[1]-=1
              if m==2: self.pos[0]-=1
              if m==3: self.pos[1]+=1
              break
          return [2, m]
        
      self.dm=self.seek(self.pos, self.goalpos)
          
      for i in range(0,4):
        temppos=[self.pos[0],self.pos[1]]
        if i==0: temppos[0]+=1
        if i==1: temppos[1]-=1
        if i==2: temppos[0]-=1
        if i==3: temppos[1]+=1
        if temppos==self.goalpos:
          #print("found goal")
          return [2,i]

      for i in self.dm:
         m = i
         if self.view[m] != 100 and m != (self.lastmove+2)%4:
            #print("not random: ", m)
            self.lastmove = m
            if m==0: self.pos[0]+=1
            if m==1: self.pos[1]-=1
            if m==2: self.pos[0]-=1
            if m==3: self.pos[1]+=1
            #print(self.goalpos)
            #print(self.view)
            return [2,m]
      #print('no moves remaining')
      return [2, (self.lastmove+2)%4]

   def feedback(self, view):
      self.view = view

