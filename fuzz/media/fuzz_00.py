# -*- coding: utf-8 -*- 
import serial       # 시리얼 통신
import time         # sleep
import signal       # exit 시그널
import threading    # threading

from os.path import isfile, join    # 파일 디렉토리
from os import listdir              # 파일 디렉토리

file_list=[]

path = "/tmp/usb/sda/LG Smart TV/"

launch_cmd = 'luna-send -n 1 -f luna://com.webos.applicationManager/launch \
\'{\"id\":\"com.webos.app.dsmp\",\"params\":{\"src\":\"/tmp/usb/sda/LG Smart \
TV/\"\'$1\'\",\"type\":\"video\"}'

l1 = "luna-send -n 1 -f luna://com.webos.applicationManager/launch \
\'{\"id\":\"com.webos.app.dsmp\",\"params\":{\"src\":"

l2 = ",\"type\":\"video\"}"

close_cmd = 'luna-send -n 1 -f luna://com.webos.applicationManager/closeByAppId\
\'{\"id\":\"com.webos.app.dsmp\"}'

path_dir="/home/jmkim/_Security/00.Fuzz/2018_Signage_Fuzz/2018_Signage_Fuzz_Data_Media/fuzzdata"

file_name=""

line = [] # 라인 단위로 데이터를 가져올 리스트 변수
port = '/dev/ttyUSB0' # 시리얼 포트
baud = 115200 # 시리얼 보드레이트 (통신속도)
exitThread = False #쓰레드 종료용 변수

# 쓰레드 종료용 시그널 함수
def handler(signum, frame):
    exitThread = True

# 데이터 처리할 함수
def parsing_data(data):
    # 리스트 구조로 들어 왔기 때문에 
    # 작업하기 편하게 스트링으로 합침
    tmp = ''.join(data)

    # 출력!
    print(tmp)

# 본 쓰레드
def readThread(ser):
    global line
    global exitThread
    
    # 쓰레드 종료될때 까지 계속 돌림
    while not exitThread:
        # 데이터가 있다면
        for c in ser.read():
            #line 변수에 차곡차곡 추가하여 넣는다.
            line.append(chr(c))

            if c == 10: #라인 끝을 만나면..
                #데이터 처리 함수로 호출
                parsing_data(line)

                #line 변수 초기화
                del line[:]


def searching(the_list, indent=False, level=0):
    print( "\n"+ the_list )

    items = listdir(the_list)
    items.sort()

    for each_item in items:
        if isfile(join(the_list, each_item)):
            if indent:
                for tab_stop in range(level):
                    print("\t", end='')
                #print(each_item)
                #print(join(the_list,each_item))
                file_list.append(join(the_list,each_item))
        else:
            searching(join(the_list, each_item), indent, level+1)

if __name__ == "__main__":

  mylist = listdir(path_dir) # ['bmp', 'rm', '3gp', 'mp4', 'jpg', 'png', 'avi', 'mkv']
  mylist.sort() #정렬

  for mypath in mylist:
    #print(join(path_dir, mypath))
    
    searching(join(path_dir, mypath), True, 1)

    #print(isfile(join(path_dir, myfile)), end=" ")
    #if isfile(join(path_dir, myfile)):
    #    print(myfile + " is FILE")
    #else:
    #    print(myfile + " is DIR")

#print(file_list)

  for i,f in enumerate(file_list):
    file_name = l1+"\""+ f +"\"" +l2
    print(i,file_name)

  # 종료 시그널 등록
  signal.signal(signal.SIGINT, handler)
  #시리얼 열기
  ser = serial.Serial(port, baud, timeout=0)
  #시리얼 읽을 쓰레드 생성
  thread = threading.Thread(target=readThread, args=(ser,))
  #시작
  thread.start()

