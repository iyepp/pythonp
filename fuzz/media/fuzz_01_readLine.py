import serial
import time
from os.path import isfile, join    # 파일 디렉토리
from os import listdir              # 파일 디렉토리

file_list=[]

ser = serial.Serial('/dev/ttyUSB0', 115200)
class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

def searching(the_list, indent=False, level=0):
    #print( "\n"+ the_list )

    items = listdir(the_list)
    items.sort()

    for each_item in items:
        if isfile(join(the_list, each_item)):
            if indent:
                #for tab_stop in range(level):
                  #print("\t", end='')
                #print(each_item)
                #print(join(the_list,each_item))
                file_list.append(join(the_list,each_item))
        else:
            searching(join(the_list, each_item), indent, level+1)

path_dir="/home/jmkim/_Security/00.Fuzz/2018_Signage_Fuzz/2018_Signage_Fuzz_Data_Media/fuzzdata"

l1 = "luna-send -n 1 -f luna://com.webos.applicationManager/launch \'{\"id\":\"com.webos.app.dsmp\",\"params\":{\"src\":"

l2 = ",\"type\":\"video\"}"

close_cmd = 'luna-send -n 1 -f luna://com.webos.applicationManager/closeByAppId \'{\"id\":\"com.webos.app.dsmp\"}'

path_dir="/home/jmkim/_Security/00.Fuzz/2018_Signage_Fuzz/2018_Signage_Fuzz_Data_Media/fuzzdata"

rl = ReadLine(ser)

#데이터를 보내자
mylist = listdir(path_dir)

for mypath in mylist: # 디렉토리 순회 하여 file_list를 만듬
    searching(join(path_dir, mypath), True, 1)

for i,f in enumerate(file_list): # file_list 출력
    file_name = l1+"\""+ f +"\"" +l2
    print(i,file_name)

print("\nstart to send... data") # sending files
for i, f in enumerate(file_list):
    time.sleep(3)
    file_name = l1+"\"" + f + "\"" +l2 +"\n"
    ser.write(file_name.encode())

#while True:
    print(rl.readline())
