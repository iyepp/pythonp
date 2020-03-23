# -*- coding: utf-8 -*-
# main procees, process A, process B
# CQ�� �����ؼ� Process�� ���� ������
import serial
import time
import io
from os.path import isfile, join  # ���� ���丮
from os import listdir  # ���� ���丮
from multiprocessing import Process, Queue
import sys # �����ϱ�
from multiprocessing.managers import BaseManager

class CQueue:
    _r = 0
    _f = 0
    _size = 0
    def __init__(self, size):
        self._list= ['']*(size+1)
        self._size = size+1
        self._r = 0
        self._f = 0

    def empty(self):
        #return True if len(self._list) == 0 else False
        return True if self._r == self._f else False

    def get(self):
        #if len(self._list) == 0 :
        if self._r == self._f :
            print(f"deQ {self._f} : {self._r} ERROR -1")
            return -1
        else:
            print(f"deQ {self._f} : {self._r} ")
            #ret = self._list.remove(self._f)
            #ret = self._list.pop(self._f)
            ret = self._list[self._f]
            print( ">>" , ret )
            self._f = (self._f+1)%self._size
            return ret

    def put(self, value):
        if (self._r+1)%self._size == self._f:
            iprint(f"enQ {self._f} : {self._r} Error -1", end="")
            return -1
        else:
            #rear�� �����ؼ� �ڿ� �ִ´�
            print(f"enQ {self._f} : {self._r} ")
            self._list[self._r] = value
            self._r = (self._r + 1) % self._size
            print("enQ << ", value)
            return value
    
    def urgent(self, value):
        #front�� ���� �ִ´�.
        self._f = (self._f-1+self._size)%self._size
        self._list[self._f] = value
        print("enQ <<<<<<<< ", value)
        return value


    def peek(self):
        #print(f"peek {self._f} : {self._r} ")
        #print( self._list[self._f] )
        return self._list[self._f]

    def checkfr(self):
        print(f"\t\t{self._f} : {self._r} ")

def myPrintTime(q):
    cnt = 0
    while True:
        cnt = cnt+1
        print(cnt)
        data = q.peek()
        if data == "SUCCESS_PROCESS":
            print("[myPrintTime] myPrintTIme is killed by SUCCESS_PROCESS msg !!!!!")
            sys.exit(0)
        elif data == "KILL_PROCESS":
            print("[myPrintTime] myPrintTIme is killed by KILL_PROCESS msg !!!!!")
            sys.exit(0)

        time.sleep(1)


def mySendRecv(myfile_list, q, sleepcount):
    #MyManager.register('q', CQueue)
    
    # 10 ���� �ֱ�� �� ���μ��� �����Ѵ�
    print("[mySendRecv] This is a Process for Action.")
    print(len(myfile_list))

    for i, f in enumerate(file_list):
        print("[", i, "]th...")
	    
        # ť�� ��� ������ ���� ���� ��ɾ �ø���� ������, �� ���� ���� ť�� �ִ´�
        if q.empty():
            print("\n[mySendRecv] Check if Q is Empty.")

            print("[mySendRecv] Sending file_full_name / Receiving file_recv._data: {}".format(f))
            q.put(f)
            q.put(f)
            # mySendRecv �� 10 �ʿ� �ѹ� ����
            print("[mySendRecv] sleep 10 ...")
            time.sleep(10)
            print()  # new line to separate another looping.
        else :
            print("\n[mySendRecv] Q is not Empty. It may cause error... Waiting until Q is Empty. for 1 sec.{} ".format(sleepcount))
            #if q.get() == -1 :
            #    break # ������ �����Ѵ�
            
            # KILL_PROCESS MSG�� ���� ��� process�� �����Ѵ�. broadcasting this message.
            msg = q.peek()
            print("[mySendRecv] peekQ  {}", msg)
            if msg.find(str("SUCCESS_PROCESS")):
               print("[mySendRecv] mySendRecv is killed by SUCCESS_PROCESS msg !!!!!")
               sys.exit(0)
            
            # temporary time
            time.sleep(1)

    # ��� �������� path�� ��� �� �����ϰ� for loop�� ���� ��������
    #q.put("[mySendRecv] SUCCESS !!! the  end of loop")
    print("[mySendRecv] SUCCESS !!! the end of loop")
    q.urgent(str("SUCCESS_PROCESS"))
    sys.exit(0)

def myMonitoring(q, sleepcount):
    #MyManager.register('q', CQueue)
    # 5 ���� �ֱ�� �� ���μ��� �����Ѵ�
    while True:
        print("\t\t[myMonitoring] This is a Process for Monitoring, checkCnt:{}".format(sleepcount))
        # while not q.empty():
            #print(q.get(),  end=' ')
        # ť�� �� ��� �´µ��� SendRecv���� ä���� ���ߴٴ� ���� SendRecv�� ������.
        if q.empty():
            print("\t\t[myMonitoring] Q is empty.")
            sleepcount = sleepcount + 1
            print("\t\tsleep 5 ...")
            time.sleep(5)

            # ������ ���°� 5���̻� ���ӵǸ� (25��)
            if sleepcount >= 5:
                # Stuck �α׸� ���
                print("\n\t\t[myMonitoring] The Action Process is stuck!!! >>>>> [-1] try to escape from this process")
                
                # KILL_PROCESS MSG�� ���� ��� process�� �����Ѵ�. broadcasting this message.
                q.urgent(str("SUCCESS_PROCESS"))
                print("[myMonitoring] Processed was killed by SUCCESS_PROCESS msg !!!!!")
                sys.exit(0) # ��� �����Ѵ�

            # ������ ���°� 5�� �̸��̸� �� Ȯ���Ѵ�.
            else:
                continue

        else: # ť�� ������� �ʾҴٸ�
            sleepcount = 0 # �缳�� sleepcount = 0 �� ������
            print("\t\t[myMonitoring] Q is not empty.")

            # ť���� �����͸� ������
            #ret_data = q.get()
            ret_data = q.get()
            print("\t\t[myMonitoring] GET ", ret_data, end="")
            print("")

            # ���̸�, �Ľ� �����Ѵ�.
            # ���� ���� ���̸�
            if ret_data == b'}\r\n':
                # comparing with  the end of luna command, '}'\\n"
                print(b'}\r\n')
                #break
                # continue # ������ ó������ 99,170

            elif ret_data == "KILL_PROCESS":
               print("\t\t[myMonitoring] Processed was killed by KILL_PROCESS msg !!!!!")
               q.urgent(str("KILL_PROCESS"))
               sys.exit(0)
            else:
                # ��Ÿ �α� ���Ƽ� ������� �ʴ� �ڵ�
                if ret_data.find('[DILE_I2C]') != -1: # ������ -1
                    continue
                # ���̰�, ���� ���� ���� �ƴϸ�, ȭ�鿡 ����Ѵ�.  �׸��� ������ �ִ��� �Ľ��� ����.
                else:
                    print(" (LEN): ", len(ret_data))
                    # ������ ������ ��������
                    if ret_data.upper().find('ERROR')  != -1: # �� ���� ������ # ��ҹ��� ���� �ʿ�
                        # ���� �α׸� ���
                        print("\n\t\t[myMonitoring] The ERROR Occurs !!! >>>>> [-1] try to escape")
                        print("[Error Log]", ret_data)

                        # ���Ͽ� ����
                        myfile = open('result.txt', 'wb')
                        
                        while not q.empty():
                            myfile.write(ret_data)
                            #ret_data = q.get()
                            ret_data = q.get()

                        myfile.flush()
                        myfile.close()
                        
                        # ������ ���� ������.
                        break #0221 LUNASEND ERROR MSG�� ���ؼ� ������ Ż���Ѵ�

                    elif ret_data.upper().find('SUCCESS_PROCESS')  != -1: # �� ���� ������
                        print("\n\t\t[myMonitoring] The test is successful !!! >>>>> [0] try to escape")
                        print("\n\n[Success Log]", ret_data)
                        break

        print("\t\t[myMonitoring] Try to check the Queue after sleep 1 ...")
        time.sleep(1)

class MyManager(BaseManager):
    pass

MyManager.register('q', CQueue)

if __name__ == '__main__':
  with MyManager() as manager:
    qq = manager.q(3)
    L1="["
    L2="]"

    global sleepcount
    sleepcount = 0
    file_list = ["A","B","C","D","E","F","G"]

    #q = CQueue(10) 
    process_A = Process(target=mySendRecv, args=(file_list, qq,sleepcount,))
    process_M = Process(target=myMonitoring, args=(qq,sleepcount,))
    process_T = Process(target=myPrintTime, args=(qq,))

    # �����͸� ������
    mylist = file_list

    # file_list ��� , target_path�� �����Ͽ� file_name�� ����
    for i, f in enumerate(file_list):
        # target
        file_name = L1 + f + L2
        
        # simulation
        print(i, file_name)
        #q.put(file_name) # �ӽ� �ڵ�� ���� ���� ���� ���� ���� ������ file_name �� ť�� �־� ����.

    #threading
    process_T.start()
    process_A.start()
    process_M.start()

    #q.close()
    #q.join_thread()

    process_T.join()
    process_A.join()
    process_M.join()

