import socketio
import requests
from person_detection_day import getserial
sio = socketio.Client()
import time


class connect():
    def __init__(self):
        #self.serial = '1122'
        self.serial = getserial()
        try:
            self.device_id = self.register()
        except:
            print("Do Not Know the ID please connect to the Internet")
            with open('./device_id.txt', 'r') as f:
                self.device_id = f.read()
                self.device_id = self.device_id[1:-1]
                f.close()
        self.id = self.serial
        self.name = self.device_id



    def register(self):
        myserial =  self.serial
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
                print("Device id is", k[1][1:-1])
                #save the device id in a text file
                device_id = k[1][1:-1]
                return device_id


    @sio.on('seq-num')
    def func(msg):
        print("Message is",msg)
        print("Writting")
        with open('./device_status.txt', 'w') as f:
            f.writelines(msg)
        f.close()


    #@sio.on('connect')
    def reg_client(self):
        print("Id is ", self.id, "Name is", self.name)
        try:
            y = sio.emit('storeClientInfo', {'customId': self.id, 'name': self.name})
            print(y)
        except:
            pass
            
        
        print('Done')


if __name__ == "__main__":

    

    while (True):
        try:
            k = sio.connect('http://156.67.216.28:8800/')
            cc = connect()
            cc.reg_client()
            #break
        except Exception as e:
            #pass
            print(e)
            
    #serial = getserial()
    # cc = connect()
    # prev_time = 0
    # while(True):
    #     current_time = time.time()
    #     if(current_time - prev_time > 10):
    #         cc.reg_client()
    #         prev_time = current_time

