import threading
import time


#global CA

def processA():
    CA = 1
    while True:
        time.sleep(1)
        print("This is processA {}".format(CA))
        CA=CA+1
def processB():
    CB = 2
    while True:
        time.sleep(2)
        print("\t\tThis is processB %d" %(CB))
        CB=CB+1
def processC():
    CC = 3
    while True:
        time.sleep(5)
        print("\t\t\t\tThis is processC %d" %(CC))
        CC=CC+1

p1 = threading.Thread(target=processA)
p2 = threading.Thread(target=processB)
p3 = threading.Thread(target=processC)

p1.start()
p2.start()
p3.start()

