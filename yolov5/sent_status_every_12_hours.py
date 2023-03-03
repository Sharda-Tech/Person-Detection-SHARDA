import time
import requests
import os

def send_request_every_12_hours(device_id):
   

    url = "http://as99.zvastica.solutions/appapi/setdevicelog"

    #payload = "{ \n \n \"device_id\" : " + device_id + " \n \n \n}"
    #status = "true"
    payload="{\n   \n \"device_id\" :" + device_id + ",\n \"status\" :\"1\"\n      \n        \n}"
    #payload="{\n   \n \"device_id\" :\"1\",\n \"status\":\"1\"\n      \n        \n}"
    print(payload)
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'ci_session=ct6c1jtts21ch70u2g4rvmj7cm06nfr3'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def check_if_12_hours(device_id):

    #if time.txt is not present, create it
    if not os.path.exists("./time.txt"):
        with open("./time.txt", "w") as f:
            f.write("")
    if not os.path.exists("./current_time.txt"):
        with open("./current_time.txt", "w") as f:
            f.write("")

    #read time.txt
    with open("./time.txt", "r") as f:
        time_string = f.read()

    if(time_string == ""):
        start_time = time.time()
        with open('./time.txt', 'w') as f:
            f.write(str(start_time))

    else:
        start_time = float(time_string)

        #save time to a file
        

    current_time = time.time()
    #write current time to a file
    with open('./current_time.txt', 'w') as f:
        f.write(str(current_time))

    if(current_time - start_time > 43200):
        print("Sent  Device Status")
        #send_request_every_12_hours(device_id)
        start_time = time.time()
        with open('./time.txt', 'w') as f:
            f.write(str(start_time))


if __name__ == "__main__":
    device_id = "1"
    check_if_12_hours(device_id)
