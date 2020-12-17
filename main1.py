from objects import elevator,floor
from random import randint
from random import shuffle
from time import sleep
import threading
#import sys
import os

#-------------variables, structures and functions will be defined here ---------------------

temp_busy_floor=5

loop_num=100

#--------------globals-----------
floors=[floor() for i in range(5)]

for n,i in enumerate(floors):
    floors[n].floor_number=n

total_elevator_queue=[] #this will always be updated, and will hold tuples(people_number, target_floor)

login_queue=[]
exit_queue=[]
elevator_list=[elevator() for i in range(5)]
#elevator_list[0].mode = True
total_elevators_working=0   
#--------//globals-----------


def list_to_tuple(liste):
    temp1=0
    temp2=0
    tuple_list=[]
    for i in range(0,5):
        for j in liste:
            if j == i:
                temp1+=1
        tuple_list.append((temp1,i))
        temp1=0
    tuple_list2=[]
    for i in tuple_list:
        if i[0] != 0:
            tuple_list2.append(i)
    
    return tuple_list2

def tuple_to_list(tuple_liste):
    liste=[]
    for i in tuple_liste:
        for j in range(i[0]):
            liste.append(i[1])
    return liste



def login():
    global floors
    x=0
  
    while(True):
        global total_elevator_queue
        total_elevator_queue = []
        queue=[]
        person_came = randint(1,11)
        for i in range(person_came):
            queue.append(randint(1,4)) 
        floors[0].queue+=queue
        
        for i in range(5):
            total_elevator_queue+=floors[i].queue
        sleep(0.5)
        
        if x == loop_num:
            break
        x+=1
    

def print_log():
    global floors
    x=0
    while(True):
        cls = lambda: os.system('clear')
        cls()
        print(f"{0}.floor-> queue: {len(floors[0].queue)}")
        for i in range(1,5):
            print(f"{i}.floor-> all:{floors[i].people_on_floor}, queue: {len(floors[i].queue)}")
        #exit_count print
        for i in elevator_list:
            print(f"active:{i.mode}")
            print(f"       mode:{i.mode}")
            print(f"       floor:{i.floor}")
            print(f"       destination:{i.destination}")
            print(f"       direction:{i.direction}")
            print(f"       capacity:{10}")
            print(f"       count_inside:{i.inside_count}")
            print(f"       inside:{list_to_tuple(i.inside)}")

        for n,i in enumerate(floors):
            if len(i.queue)!=0:
                print(f"{n}. floor : {list_to_tuple(i.queue)} -- {len(i.queue)}")
            else:
                print(f"{n}. floor : {(i.queue)}")
        sleep(0.5)

        if x == loop_num:
            break
        x+=1




def find_busiest():
    global floors,elevator_list
    busy_floor=0
    temp_floor_queue_n=0
    for n,i in enumerate(floors): #finding the busiest floor
        if len(i.queue) > temp_floor_queue_n:
            temp_floor_queue_n = len(i.queue) # en yoğun kat
            busy_floor = n
    return busy_floor
    
def find_direction(index):
    global elevator_list,floors
    if elevator_list[index].floor > find_busiest():
        return -1
    if elevator_list[index].floor == find_busiest():
        return 0
    if elevator_list[index].floor < find_busiest():
        return 1

def run_elevator(index): #0,1,2,3,4
    global temp_busy_floor  #global anahtar kelimesi  fonksiyon dışında tanımlanmış değişkeni sadece okuma modunda değil aynı zamanda yazma modunda kullanır.
    global floors
    global elevator_list
    global total_elevators_working
    global total_elevator_queue
    
    temp_floor_queue_n=0
    a=0;b=0;c=0;d=0
    busy_floor=0
    second_busy=5
    x=0
    while(x<loop_num): #when elevator works
        temp_busy_floor = find_busiest()

        if elevator_list[index].mode == True: # if elevator active

            if elevator_list[index].inside_count == 0: #içi boşsa
                if find_busiest() == 0: # 0.kattatn adam alacaksa
                    elevator_list[index].move(find_busiest())
                    elevator_list[index].take_people(floors[ elevator_list[index].floor ].queue )
                else: # üst katlardan adam alcakasa
                    while(elevator_list[index].inside_count != 10):
                        if(find_busiest()!=0):
                            elevator_list[index].move(find_busiest())
                            elevator_list[index].take_people(floors[ elevator_list[index].floor ].queue)
            
            else: # içi boş değilse
                if elevator_list[index].inside != []:
                    if elevator_list[index].inside[0] != 0: # içindekiler 0.kata inmek istemiyorsalar
                        for i in range(1,5):
                            if i in elevator_list[index].inside:
                                elevator_list[index].move(i)
                                floors[i].people_on_floor+=elevator_list[index].leave_people()
                        pass

                    else: # içindekiler sıfıra inmek istiyorsalar
                        elevator_list[index].move(0)
                        elevator_list[index].deletePeople()
                        pass



            
        if(elevator_list[index].mode == False): # if elevator is inactive
            if elevator_list[index].inside_count!=0:
                if elevator_list[index].inside[0] != 0: # içindekiler 0.kata inmek istemiyorsalar
                        for i in range(1,5):
                            if i in elevator_list[index].inside:
                                elevator_list[index].move(i)
                                floors[i].people_on_floor+=elevator_list[index].leave_people()
                        pass

                else: # içindekiler sıfıra inmek istiyorsalar
                    elevator_list[index].move(0)
                    elevator_list[index].deletePeople()
                    pass
            else:
                pass
        
        sleep(0.5) ## (program çalışır hale geldiğinde kaldırılacak.)
        x+=1

        


def elevator_check():
    global elevator_list
    global total_elevators_working
    global total_elevator_queue
    x=0
    while(x<loop_num):

        if total_elevators_working*10 > len(total_elevator_queue):
            if total_elevators_working>1:
                elevator_list[total_elevators_working-1].mode = False
                total_elevators_working-=1
        
        if total_elevators_working*10 < len(total_elevator_queue)*2:
            if total_elevators_working < 5:
                elevator_list[total_elevators_working].mode=True
                total_elevators_working+=1

        sleep(0.5)
        x+=1     
    
  #time.sleep(0.5)

def smaller(a,b):
    if a>b:
        return b
    else:
        return a

def exit(): # as a thread (sadece random olarak çıkmak isteyen insan üretip onları kendi katında asansör kuyruğuna alacak.)
    global floors
    queue=[]
    fl_list=[]
    
    x=0
    while(x<loop_num/2):
        leng=0
        #katlardan random 5 insanı seçecek.(katlardaki insan sayısı göz önüne alınarak)
        
        rand_num = randint(1,5)

            ##katlardan çıkıcak kişileri rastgele seçerken o kattaki insan sayısını aşmayacak şekilde olmalı.
        fl_list=[i for i in range(1,5)]
        shuffle(fl_list) #== katların random sıralanmış listesi

        while(leng<=rand_num): # bir döngüde beşe ulaşana kadar.
            for i in fl_list:
                x=randint(0,smaller(rand_num,floors[i].people_on_floor))
                leng+=x
                for k in range(x):
                    floors[i].queue.append(0)
                    floors[i].people_on_floor -= 1

        sleep(1)
        x+=1

if __name__ == "__main__":
  
  ## program will run on the public variables. i will not need to return any value from any function(thread)
    login_t = threading.Thread(target=login,args=())
    print_t = threading.Thread(target=print_log,args=())
    elevator_check_t=threading.Thread(target=elevator_check,args=())
    elevator_run_0_t = threading.Thread(target=run_elevator,args=[0])
    elevator_run_1_t = threading.Thread(target=run_elevator,args=[1])
    elevator_run_2_t = threading.Thread(target=run_elevator,args=[2])
    elevator_run_3_t = threading.Thread(target=run_elevator,args=[3])
    elevator_run_4_t = threading.Thread(target=run_elevator,args=[4])
    exit_t=threading.Thread(target = exit, args=())

    login_t.start() #thread1

    elevator_check_t.start() #thread2

    elevator_run_0_t.start() #-
    elevator_run_1_t.start() #-
    elevator_run_2_t.start() #- thread3
    elevator_run_3_t.start() #-
    elevator_run_4_t.start() #-

    exit_t.start() # thread4

    print_t.start()