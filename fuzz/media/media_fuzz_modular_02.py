import serial
import time
import io
from os.path import isfile, join  # 파일 디렉토리
from os import listdir  # 파일 디렉토리
# added the starting section where user want to start point. v0.2

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i + 1]
            self.buf = self.buf[i + 1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i + 1]
                self.buf[0:] = data[i + 1:]
                return r
            else:
                self.buf.extend(data)

def searching(the_list, indent=False, level=0):
    # print( "\n"+ the_list )

    items = listdir(the_list)
    items.sort()

    for each_item in items:
        if isfile(join(the_list, each_item)):
            if indent:
                # for tab_stop in range(level):
                # print("\t", end='')
                # print(each_item)
                # print(join(the_list,each_item))
                file_list.append(join(the_list, each_item))
        else:
            searching(join(the_list, each_item), indent, level + 1)

# if __name__ == '__main__':

""" References of luna-send
#luna-send -n 1 -f luna://com.webos.applicationManager/launch '{"id":"com.webos.app.dsmp","params":{"src":"/tmp/usb/sda/sda1/LG Smart TV/1.mp4","type":"video"}'
#luna-send -n 1 -f luna://com.webos.applicationManager/closeByAppId '{ "id": "com.webos.app.dsmp" }'
#luna-send -n 1 -f luna://com.webos.applicationManager/running '{}'

# just in case
close_cmd = 'luna-send -n 1 -f luna://com.webos.applicationManager/closeByAppId \'{\"id\":\"com.webos.app.dsmp\"}'
pop = "luna-send -n 1 -f luna://com.webos.service.pqcontroller/setDebuggingData '{\"alertPopup\":5}'"

"""

ser = serial.Serial('/dev/ttyUSB0', 115200)
target_path ="/tmp/usb/sda/sda1/sample_video_100000"
local_path ="/home/jmkim/usb3"

file_list = []
path_dir = local_path

#L1 = "luna-send -n 1 -f luna://com.webos.applicationManager/launch \'{\"id\":\"com.webos.app.dsmp\",\"params\":{\"src\":"
L1 = "luna-send -n 1 -f luna://com.webos.applicationManager/launch \'{\"id\":\"com.webos.app.ism\",\"params\":{\"mode\":\"userMovie\",\"userdata\": { \"moviepath\": [\""
#l2 = ",\"type\":\"video\"}\'"
L2 = "\"]}}}\'"

MAX_NUMBER=0

# 데이터를 보내자
mylist = listdir(path_dir) # local_path로 file_list를 생성함

for mypath in mylist:  # 디렉토리 순회 하여 file_list를 만듬
    searching(join(path_dir, mypath), True, 1)

for i, f in enumerate(file_list):  # file_list 출력 , target_path로 변경하여 file_name을 뽑음
    # target
    tempString = f.split('/')
    tempString = tempString[-1:]
    tempString = join(target_path, tempString[0])
    file_name = L1 + tempString + L2
    # simulation
    #file_name = l1 + "\"" + f + "\"" + l2
    print(i, file_name)
    MAX_NUMBER = i

#몇번째 부터 시작을 할지 입력을 받는다.
startpoint = int(input("Start Point(0~{}) :".format(MAX_NUMBER)))

for i, f in enumerate(file_list):
    if  i < startpoint :
        print("[", i, "] skipped...")
        continue
    time.sleep(10)
    print("[", i, "]")

    #file_name = l1 + "\"" + f + "\"" + l2 + "\n"
    tempString = f.split('/')
    tempString = tempString[-1:]
    tempString = join(target_path, tempString[0])
    file_name = L1 + tempString + L2 + "\n"

    # print("[in]", file_name)
    # file_name = l1+f+l2+"\n"
    # print( i, file_name)
    # ser.write(bytes(bytearray(0x0D)))
    ser.write(file_name.encode('utf-8'))
#    ser.write(pop.encode('utf-8'))

    # sio.write(file_name.encode('utf-8'))
    # sio.flush()

    while True:
        ret_data = ser.readline()

        if ret_data == b'}\r\n':
            # comparing with  the end of luna command, '}'\\n"
            print(b'}\r\n')
            break

        else:
            if ret_data.find(b'[DILE_I2C]') != -1:
                # if ret_data.find(b'error'):
                #     print("ERROR Occured\n", file_name)
                #     print(ret_data)
                #     print("<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                #     break;
                continue
            else:
                print(ret_data, " : ", len(ret_data))
    print() # new line to separate another looping.


