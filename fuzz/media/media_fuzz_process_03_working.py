# -*- coding: utf-8 -*-
# main procees, process A, process B
# CQ를 정의해서 Process간 공유 성공함
import serial
import time
import io
from os.path import isfile, join  # 파일 디렉토리
from os import listdir  # 파일 디렉토리
from multiprocessing import Process, Queue
import sys # 종료하기
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
            #rear를 증가해서 뒤에 넣는다
            print(f"enQ {self._f} : {self._r} ")
            self._list[self._r] = value
            self._r = (self._r + 1) % self._size
            print("enQ << ", value)
            return value
    
    def urgent(self, value):
        #front에 빼서 넣는다.
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
    
    # 10 초의 주기로 이 프로세는 동작한다
    print("[mySendRecv] This is a Process for Action.")
    print(len(myfile_list))

    for i, f in enumerate(file_list):
        print("[", i, "]th...")
	    
        # 큐가 비어 있으면 다음 실행 명령어를 시리얼로 보내고, 그 리턴 값을 큐에 넣는다
        if q.empty():
            print("\n[mySendRecv] Check if Q is Empty.")

            print("[mySendRecv] Sending file_full_name / Receiving file_recv._data: {}".format(f))
            q.put(f)
            q.put(f)
            # mySendRecv 는 10 초에 한번 돈다
            print("[mySendRecv] sleep 10 ...")
            time.sleep(10)
            print()  # new line to separate another looping.
        else :
            print("\n[mySendRecv] Q is not Empty. It may cause error... Waiting until Q is Empty. for 1 sec.{} ".format(sleepcount))
            #if q.get() == -1 :
            #    break # 루프를 종료한다
            
            # KILL_PROCESS MSG가 있을 경우 process를 종료한다. broadcasting this message.
            msg = q.peek()
            print("[mySendRecv] peekQ  {}", msg)
            if msg.find(str("SUCCESS_PROCESS")):
               print("[mySendRecv] mySendRecv is killed by SUCCESS_PROCESS msg !!!!!")
               sys.exit(0)
            
            # temporary time
            time.sleep(1)

    # 모든 동영상의 path를 모두 잘 전달하고 for loop를 빠져 나왔으면
    #q.put("[mySendRecv] SUCCESS !!! the  end of loop")
    print("[mySendRecv] SUCCESS !!! the end of loop")
    q.urgent(str("SUCCESS_PROCESS"))
    sys.exit(0)

def myMonitoring(q, sleepcount):
    #MyManager.register('q', CQueue)
    # 5 초의 주기로 이 프로세는 동작한다
    while True:
        print("\t\t[myMonitoring] This is a Process for Monitoring, checkCnt:{}".format(sleepcount))
        # while not q.empty():
            #print(q.get(),  end=' ')
        # 큐를 다 쏟아 냈는데도 SendRecv에서 채우지 못했다는 것은 SendRecv가 무한임.
        if q.empty():
            print("\t\t[myMonitoring] Q is empty.")
            sleepcount = sleepcount + 1
            print("\t\tsleep 5 ...")
            time.sleep(5)

            # 무응답 상태가 5번이상 지속되면 (25초)
            if sleepcount >= 5:
                # Stuck 로그를 찍고
                print("\n\t\t[myMonitoring] The Action Process is stuck!!! >>>>> [-1] try to escape from this process")
                
                # KILL_PROCESS MSG가 있을 경우 process를 종료한다. broadcasting this message.
                q.urgent(str("SUCCESS_PROCESS"))
                print("[myMonitoring] Processed was killed by SUCCESS_PROCESS msg !!!!!")
                sys.exit(0) # 모두 종료한다

            # 무응답 상태가 5번 미만이면 재 확인한다.
            else:
                continue

        else: # 큐가 비어지지 않았다면
            sleepcount = 0 # 재설정 sleepcount = 0 로 세팅함
            print("\t\t[myMonitoring] Q is not empty.")

            # 큐에서 데이터를 꺼내서
            #ret_data = q.get()
            ret_data = q.get()
            print("\t\t[myMonitoring] GET ", ret_data, end="")
            print("")

            # 참이면, 파싱 시작한다.
            # 리턴 값의 끝이면
            if ret_data == b'}\r\n':
                # comparing with  the end of luna command, '}'\\n"
                print(b'}\r\n')
                #break
                # continue # 루프의 처음으로 99,170

            elif ret_data == "KILL_PROCESS":
               print("\t\t[myMonitoring] Processed was killed by KILL_PROCESS msg !!!!!")
               q.urgent(str("KILL_PROCESS"))
               sys.exit(0)
            else:
                # 기타 로그 많아서 출력하지 않는 코드
                if ret_data.find('[DILE_I2C]') != -1: # 없으면 -1
                    continue
                # 참이고, 리턴 값의 끝이 아니면, 화면에 출력한다.  그리고 에러가 있는지 파싱해 본다.
                else:
                    print(" (LEN): ", len(ret_data))
                    # 에러가 있으면 종료힌다
                    if ret_data.upper().find('ERROR')  != -1: # 뭔 가가 있으면 # 대소문자 구분 필요
                        # 에러 로그를 찍고
                        print("\n\t\t[myMonitoring] The ERROR Occurs !!! >>>>> [-1] try to escape")
                        print("[Error Log]", ret_data)

                        # 파일에 쓴다
                        myfile = open('result.txt', 'wb')
                        
                        while not q.empty():
                            myfile.write(ret_data)
                            #ret_data = q.get()
                            ret_data = q.get()

                        myfile.flush()
                        myfile.close()
                        
                        # 루프를 빠져 나간다.
                        break #0221 LUNASEND ERROR MSG에 의해서 루프를 탈출한다

                    elif ret_data.upper().find('SUCCESS_PROCESS')  != -1: # 뭔 가가 있으면
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

    # 데이터를 보내자
    mylist = file_list

    # file_list 출력 , target_path로 변경하여 file_name을 뽑음
    for i, f in enumerate(file_list):
        # target
        file_name = L1 + f + L2
        
        # simulation
        print(i, file_name)
        #q.put(file_name) # 임시 코드로 보드 동작 하지 않을 때는 각각의 file_name 을 큐에 넣어 본다.

    #threading
    process_T.start()
    process_A.start()
    process_M.start()

    #q.close()
    #q.join_thread()

    process_T.join()
    process_A.join()
    process_M.join()

