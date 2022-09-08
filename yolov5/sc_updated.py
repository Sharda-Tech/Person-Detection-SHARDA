import socketio
import requests
from person_detection_day import getserial
sio = socketio.Client()





def register(serial):
    myserial =  serial
    #myserial = "0013"
    url = "http://as99.zvastica.solutions/appapi/adddevicebyhardware"

    #payload="{\n   \n \"hardwar_id\" :\"devicde_serial_no\"\n      \n        \n}"
    payload = "{ \n \n \"hardwar_id\" : \"" + myserial + "\" \n \n \n}"
    print(payload)
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'ci_session=jsunnmfv9mlfgs7cbcu0nlt8rg2op8up'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    #split string using ','
    str = response.text.split(',')
    for i in str:
        #print(i)
        k = i.split(':')   
        if(k[0] == '{"device_id"'):
            #print("Device is not registered")
            print("Device id is", k[1])
            #save the device id in a text file
            device_id = k[1]
            return device_id


@sio.on('seq-num')
def func(msg):
    print("Message is",msg)
    print("Writting")
    with open('./device_status.txt', 'w') as f:
        f.writelines(msg)
    f.close()


@sio.on('connect')
def reg_client(id, name):
    print("Id is ", id, "Name is", name)
    sio.emit('storeClientInfo', {'customId': id, 'name': name})
    print('Done')


if __name__ == "__main__":

    while (True):
        try:
            sio.connect('http://156.67.216.28:8800/')
            break
        except:
            print("Retrying")
            continue
    serial = getserial()
    #serial = "1112233"
    try:
        device_id = register(serial)
    except:
        print("Do Not Know the ID please connect to the Internet")
        with open('/home/pi/Person-Detection/yolov5/device_id.txt', 'r') as f:
            device_id = f.read()
            f.close()
    id = serial
    name = device_id
    reg_client(id, name)

