import socketio

sio = socketio.Client()


@sio.on('seq-num')
def func(msg):
    print("Message is",msg)
    print("Writting")
    with open('/home/pi/Person-Detection-SHARDA/yolov5/device_status.txt', 'w') as f:
        f.writelines(msg)
    f.close()

sio.connect('http://156.67.216.28:8800/')