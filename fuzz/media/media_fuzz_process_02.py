import serial
import time
import io
from os.path import isfile, join  # 파일 디렉토리
from os import listdir  # 파일 디렉토리
from multiprocessing import Process, Queue
sentinel = -1

def searching(the_list, indent=False, level=0):
    items = listdir(the_list)
    items.sort()
    for each_item in items:
        if isfile(join(the_list, each_item)):
            if indent:
                file_list.append(join(the_list, each_item))
        else:
            searching(join(the_list, each_item), indent, level + 1)
def mySendRecv(ser, myfile_list, q):
    print("This is Process Action")
    print(len(myfile_list))

    for i, f in enumerate(file_list):
        print("[", i, "]")

        tempString = f.split('/')
        tempString = tempString[-1:]
        tempString = join(target_path, tempString[0])
        file_name = L1 + tempString + L2 + "\n"

        #ser.write(file_name.encode('utf-8'))
        ser.write(b'ls -al\n')

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
        print()  # new line to separate another looping.

    return ''

def myMonitoring(ser, q):

    while True:
        ser.write(b'ls -al\n')
        print("\t\tThis is Process for Monitoring")
        ret_data = ser.readline()

        print("\t\t[Monitoring]", ret_data)

        time.sleep(10)

    return ''

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    target_path ="/tmp/usb/sda/sda1/sample_video_100000"
    local_path ="/home/jmkim/usb2"
    
    L1 = "luna-send -n 1 -f luna://com.webos.applicationManager/launch \'{\"id\":\"com.webos.app.ism\",\"params\":{\"mode\":\"userMovie\",\"userdata\": { \"moviepath\": [\""
    L2 = "\"]}}}\'"
    
    file_list = []
    path_dir = local_path

    q = Queue()
    process_A = Process(target=mySendRecv, args=(ser, file_list,q))
    process_M = Process(target=myMonitoring, args=(ser, q,))


    # 데이터를 보내자
    mylist = listdir(path_dir) # local_path로 file_list를 생성함

    for mypath in mylist:  # 디렉토리 순회 하여 file_list를 만듬
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
        #q.put(file_name)

    #threading
    process_A.start()
    process_M.start()

    q.close()
    q.join_thread()

    process_A.join()
    process_M.join()




