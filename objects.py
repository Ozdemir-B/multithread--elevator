
#from code.main1 import list_to_tuple, tuple_to_list
from random import randint
from time import sleep
import threading

#---------------------------classes will be defined here--------------------------

class elevator:
  def __init__(self):
    self.capacity = 10
    self.mode = False #false for not working, true for working
    self.destination=0 # floor that elevator going 
    self.direction = 1 # -1 for down and 1 for up and 0 for still
    self.inside = [] # yuple list of (int(number of people),int(target floor))
    self.inside_count=len(self.inside) # number of people inside elevator
    self.floor = 1 # floor number that elevator in
    
  def list_to_tuple(self,liste):
    temp1=0
    temp2=0
    tuple_list=[]
    for i in range(1,5):
        for j in liste:
            if j == i:
                temp1+=1
        tuple_list.append((temp1,i))
        temp1=0
    return tuple_list

  def tuple_to_list(self,tuple_liste):
    liste=[]
    for i in tuple_liste:
        for j in range(i[0]):
            liste.append(i[1])
    return liste

  def take_people(self,queue):
    if self.floor == 0:
      for i in range(len(queue)):
        self.inside.append(queue.pop(0))
        self.inside_count+=1
        if self.inside_count == 10:
          break
        if i == len(queue) -1:
          i=0

    else:
      if len(queue) <= self.capacity-self.inside_count:
        for i in queue:
          self.inside_count+=1
        self.inside += queue
        queue.clear()
      if len(queue) > self.capacity-self.inside_count:
        for i in range(self.capacity - self.inside_count):
          self.inside_count+=1
          self.inside.append(queue.pop(0))       
  
  def deletePeople(self):
    self.inside.clear()
    self.inside_count=len(self.inside)
  
  def leave_people(self): #bir kattaki queueye asansörden insan bırakıyor.
      #floor_number is floor that elevator on
    leaving_number = 0
    for n,i in enumerate(self.inside):
      if i == self.floor:
        leaving_number+=1
    while self.floor in self.inside:
      for n,i in enumerate(self.inside):
        if i == self.floor:
          self.inside.pop(n)
    self.inside_count = len(self.inside)
    return leaving_number

  def move(self,dest=0): #val an be -1, 1, and 0
    self.destination = dest
    if self.destination > self.floor:
      self.direction = 1
    if self.destination == self.floor:
      self.direction = 0
    if self.destination < self.floor:
      self.direction = -1

    for i in range( abs( self.destination - self.floor ) ):  
      self.floor+=self.direction
      if self.floor == self.destination:
        self.direction = 0
      if self.direction != 0:
        sleep(0.2)


class floor:
  def __init__(self):
    self.floor_number=0
    self.people_on_floor=0
    self.queue=[]