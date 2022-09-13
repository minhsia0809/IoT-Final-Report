import paho.mqtt.client as mqtt
import threading
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

temp,x,y = [],[],[]
fig = plt.figure()
axis = plt.axes(xlim = (-100,800) , ylim = (-100,800))
axis.set_xlabel("cm")
axis.set_ylabel("cm")
axis.set_title("UWB Test")
int_x = [[0,1],[0,1],[386,387],[386,387]]
int_y = [[0,1],[485,486],[0,1],[485,486]]
line, = axis.plot([],[],lw = 5,label="label")
line2, = axis.plot([],[],lw = 3,label="Ancher A")
line3, = axis.plot([],[],lw = 3,label="Ancher B")
line4, = axis.plot([],[],lw = 3,label="Ancher C")
line5, = axis.plot([],[],lw = 3,label="Ancher D")
axis.legend(loc="upper right")

def init(): 
    line.set_data([],[])
    line2.set_data([],[])
    line3.set_data([],[])
    line4.set_data([],[])
    line5.set_data([],[])
    return line,line2,line3,line4,line5,
   
def animate(i):
    if len(x) > 0 and len(y) > 0 :
        line.set_data(x,y)
    line2.set_data(int_x[0], int_y[0])
    line3.set_data(int_x[1], int_y[1])
    line4.set_data(int_x[2], int_y[2])
    line5.set_data(int_x[3], int_y[3])   
    return line,line2,line3,line4,line5,

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):    
    xy = str(msg.payload.decode())
    if xy.startswith('Rtls') :  
        temp = xy[5:].strip().split(" ")
        try :
            if len(temp) == 9 :
                print('X = %d , Y = %d' %(int(temp[2]),int(temp[7])))
                x.append(int(temp[2]))
                y.append(int(temp[7]))
                if len(x) > 2 :
                    x.pop(0)
                if len(y) > 2 :
                    y.pop(0)
        except Exception as ex :
            print(str(ex))

def mqtt_connect():
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.connect("140.127.220.208", 1883, 60)
    mqttc.subscribe("a1083301", 0)
    mqttc.loop_forever()

t = threading.Thread(target = mqtt_connect)
t.start()
anim = animation.FuncAnimation(fig, animate, init_func = init, frames = 200, interval = 20, blit = True)
plt.show()