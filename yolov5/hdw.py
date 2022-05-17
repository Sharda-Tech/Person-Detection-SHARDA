import requests

def register():
    myserial = "10000000d524b260"
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
            with open('device_id.txt', 'w') as f:
                f.write(device_id)
                f.close()
            return "Device id written to file"


if __name__ == '__main__':
    register()

