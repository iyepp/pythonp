# -*- conding: utf-8 -*-
import serial # pyserial 라이브러리 가져오기
def sendData(x,y):
    # 1 Byte 보내기 16진수 0xC0 보내기
    #ser.write(bytes(bytearray([0xC0])))
    # 1 Byte 보내기 매개변수로 받은 x 값 보내기
    ser.write(bytes(bytearray([x])))
    # 1 Byte 보내기 매개변수로 받은 y 값 보내기
    ser.write(bytes(bytearray([y])))


#시리얼 열기 보드레이트 9600
ser = serial.Serial('/dev/ttyUSB0', 115200)
print(ser.portstr) # 연결된 포트 확인
#sendData함수를 호출하여 시리얼 데이터 보내기
#sendData(0x0D,0x7F) #10진수로 넣어도 동일한 결과가 나타난다.
# sendData(0x72, 0x65) # re
# sendData(0x73, 0x65) #   se
# sendData(0x74, 0x0D) #     t <enter>

# sendData(0x72, 0x65) # re
# sendData(0x62, 0x6F) #   bo
# sendData(0x6F, 0x74) #     ot
# sendData(0x0D, 0x0D) #        <enter>
#sendData('a','b','c')

cmd = "luna-send -n 1 -f luna://com.webos.applicationManager/getForegroundAppInfo '{\"subscribe\":true}'"
#cmd = "luna-send -n 1 -f luna://com.webos.applicationManager/launch '{\"id\":\"com.webos.app.dsmp\",\"params\":{\"src\":\"/tmp/usb/sda/sda2/LG Smart TV/'1'\",\"type\":\"video\"}}'"
#cmd = "luna-send -n 1 -f luna://com.webos.applicationManager/launch '{\"id\":\"com.webos.app.dsmp\",\"params\":{\"src\":\"/tmp/usb/1.mp4\",\"type\":\"video\"}}'"
ser.write(bytes(cmd, encoding='ascii')) #출력방식1
sendData(0x0D, 0x0D)

#시리얼 포트 닫기
ser.close()
