import serial
import time
import io

infile=open("commands.txt","r")
cmds = infile.readlines()

ser = serial.Serial('/dev/ttyUSB1', 115200)

outfile=open("result_temp.txt","w")
i=0
for cmd in cmds:
    print(cmd)

    if cmd.upper().find('LUNA-SEND') != -1 :
        if cmd.find('#') != 0:
            i=i+1
            idxStr =  '['+ str(i) + ']'
            outfile.write( idxStr )
            outfile.write( '\r\n' )
   
            #outfile.write( str(cmd) )
            #outfile.write( '\r\n' )
            ser.write(cmd.encode('utf-8'))
        
            while True:
                ret_data = ser.readline()
	
                if ret_data == b'}\r\n':
                    # comparing with  the end of luna command, '}'\\n"
                    outfile.write('}\r\n')
                    break;
                elif ret_data.find(b'[DILE_I2C]') != -1:
                    continue;
                else:
                    outfile.write( str(ret_data) )
                    outfile.write( '\r\n' )
        else:
            outfile.write( str(cmd))
    else:	
        outfile.write( str(cmd) )
        #outfile.write( '\r\n' )
infile.close()
outfile.close()
