#import io
import serial
#import sys
import time
import paho.mqtt.client as mqtt




ser = serial.Serial(port='COM4',
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=0.5,
        xonxoff=False,
        rtscts=False,
        dsrdtr=False)



try:
    ser.open()
except Exception as ex:
    print(ex)

if ser.isOpen():
    try:
        s = []
        ser.flushInput()
        ser.flushOutput()
        #signal_text = io.TextIOWrapper(ser, newline='\r\n')
        #ser.write('AT\r\n'.encode())        
        #print('OK?', ser.readline())
        #ser.write('AT+switchdis=1\r\n'.encode())
        #print('AT: ', ser.readline())
        

        client = mqtt.Client()
        try:
            client.connect("140.127.220.208", 1883, 60)
        except:
            print("not connect")


        while True:
#            ser.write('AT+PrintMode=0 , 1\r\n'.encode())
#            ser.write('AT+DataSend= , 255 ')
            
            datas = ser.readline()
            #mqtt connect

            client.publish("a1083301", datas)
            print("ok")
            time.sleep(0.05)

            print(datas)

    except Exception as ex:
        print('weed2')
    finally:
        ser.close()

else:
    print('+hello')



