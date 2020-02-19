# main process, process A, process B
import serial
import time
import io
from os.path import isfile, join  # 파일 디렉토리
from os import listdir  # 파일 디렉토리
from multiprocessing import Process, Queue
import sys # 종료하기

sentinel = -1
def stuckExit(self):
    sys.exit(0)

def searching(the_list, indent=False, level=0):
    items = listdir(the_list)
    items.sort()
    for each_item in items:
        if isfile(join(the_list, each_item)):
            if indent:
                file_list.append(join(the_list, each_item))
        else:
            searching(join(the_list, each_item), indent, level + 1)
def myPrintTime():
    cnt = 0
    while True:
        cnt = cnt+1
        print(cnt)
        time.sleep(1)


def mySendRecv(ser, myfile_list, q, sleepcount):
    # 10 초의 주기로 이 프로세는 동작한다
    print("[mySendRecv] This is a Process for Action.")
    print(len(myfile_list))

    for i, f in enumerate(file_list):
        print("[", i, "]th...")

        tempString = f.split('/')
        tempString = tempString[-1:]
        tempString = join(target_path, tempString[0])
        file_name = L1 + tempString + L2 + "\n"

        ser.write(file_name.encode('utf-8'))
        #ser.write(b'ls -al\n')



        #print("[mySendRecv] sleepcount {}".format(sleepcount))
        # while True:
        #     # serial 리턴 값으 읽어서
        #     ret_data = ser.readline()
        #
        #     # 큐 에다 넣는다(넣을만한 스트링만)
        #     q.put(ret_data)

        if q.empty():
            print("\n[mySendRecv] Check if Q is Empty.")
            # for testing
            q.put(file_name)

            print("\n[mySendRecv] Sending file_full_name / Receiving file_recv._data\n")

            # mySendRecv 는 10 초에 한번 돈다
            print("[mySendRecv] sleep 10 ...")
            time.sleep(10)
            print()  # new line to separate another looping.
        else :
            print("\n[mySendRecv] Q is not Empty. Waiting until Q is Empty. for 1 sec. ")
            # temporary time
            time.sleep(1)

    # 모든 동영상의 path를 모두 잘 전달하고 for loop를 빠져 나왔으면
    q.put("[mySendRecv] SUCCESS !!! the end of loop")

def myMonitoring(ser, q, sleepcount):
    # 5 초의 주기로 이 프로세는 동작한다
    while True:
        print("\t\t[myMonitoring] This is a Process for Monitoring, checkCnt:{}".format(sleepcount))
        # while not q.empty():
            #print(q.get(),  end=' ')
        if q.empty():
            print("\t\t[myMonitoring] Q is empty.")
            sleepcount = sleepcount + 1
            print("\t\tsleep 5 ...")
            time.sleep(5)

            # 무응답 상태가 5번이상 지속되면 (25초)
            if sleepcount >= 5:
                # Stuck 로그를 찍고
                print("\n\t\t[myMonitoring] The Action Process is stuck!!! >>>>> [-1] try to escape from this process")
                # 루프를 빠져 나간다
                break

            # 무응답 상태가 5번 미만이면 재 확인한다.
            else:
                continue

        else: # 큐가 비어지지 않았다면
            sleepcount = 0 # 재설정 sleepcount = 0 로 세팅함
            print("\t\t[myMonitoring] Q is not empty.")

            # 큐에서 데이터를 꺼내서
            ret_data = q.get()
            print("\t\t[myMonitoring] GET ", ret_data, end="")
            print("")

            # 참이면, 파싱 시작한다.
            # 리턴 값의 끝이면
            if ret_data == b'}\r\n':
                # comparing with  the end of luna command, '}'\\n"
                print(b'}\r\n')
                #break
                continue # 루프의 처음으로

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

                        # 루프를 빠져 나간다.
                        break
                    elif ret_data.upper().find('SUCCESS')  != -1: # 뭔 가가 있으면
                        print("\n\t\t[myMonitoring] The test is successful !!! >>>>> [0] try to escape")
                        print("\n\n[Success Log]", ret_data)
                        break

        print("\t\t[myMonitoring] Try to check the Queue after sleep 1 ...")
        time.sleep(1)
    sys.exit(0)

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    target_path ="/tmp/usb/sda/sda1/sample_video_100000"
    local_path ="/home/jmkim/usb3"
    
    L1 = "luna-send -n 1 -f luna://com.webos.applicationManager/launch \'{\"id\":\"com.webos.app.ism\",\"params\":{\"mode\":\"userMovie\",\"userdata\": { \"moviepath\": [\""
    L2 = "\"]}}}\'"

    global sleepcount
    sleepcount = 0
    file_list = []
    path_dir = local_path

    q = Queue()
    process_A = Process(target=mySendRecv, args=(ser, file_list,q, sleepcount))
    process_M = Process(target=myMonitoring, args=(ser, q,sleepcount, ))
    process_T = Process(target=myPrintTime)

    # 데이터를 보내자
    mylist = listdir(path_dir) # local_path로 file_list를 생성함

    for mypath in mylist:  # 디렉토리 순회 하여 file_list를 만듦
        searching(join(path_dir, mypath), True, 1)


    # file_list 출력 , target_path로 변경하여 file_name을 뽑음
    for i, f in enumerate(file_list):
        # target
        tempString = f.split('/')
        tempString = tempString[-1:]
        tempString = join(target_path, tempString[0])
        file_name = L1 + tempString + L2
        
        # simulation
        print(i, file_name)
        #q.put(file_name) # 임시 코드로 보드 동작 하지 않을 때는 각각의 file_name 을 큐에 넣어 본다.

    #threading
    process_T.start()
    process_A.start()
    process_M.start()


    q.close()
    q.join_thread()

    process_T.join()
    process_A.join()
    process_M.join()




