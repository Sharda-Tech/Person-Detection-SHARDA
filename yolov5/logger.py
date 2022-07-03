import requests
import time
import os

def log_sent(device_id, status):
    url = "http://as99.zvastica.solutions/appapi/setreport"


    #payload="{\n   \n \"device_id\" :\"" + device_id + "\",\n \"status\" :\"1\"\n      \n        \n}"

    payload = "{\n   \n \"device_id\" :" + device_id + ",\n \"event\" :\"" + status + "\"\n      \n        \n}"
    #payload="{\n   \n \"device_id\" :\"1\",\n \"event\":\"sdsddsd1\"\n      \n        \n}"

    print(payload)
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'ci_session=ct6c1jtts21ch70u2g4rvmj7cm06nfr3'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def log_data(device_id):
    
    current_time = time.time()
    #create current time file if it doesn't exist
    if not os.path.exists("/home/pi/Person-Detection/yolov5/current_time.txt"):
        with open("/home/pi/Person-Detection/yolov5/current_time.txt", "w") as f:
            f.write("")


    #read current time file
    with open("/home/pi/Person-Detection/yolov5/current_time.txt", "r") as f:
        time_string = f.read()

    if(time_string == ""):
        current_time = time.time()
        with open('/home/pi/Person-Detection/yolov5/current_time.txt', 'w') as f:
            f.write(str(current_time))


    if(time_string != ""):
        time_read_from_file = float(time_string)
    if(current_time - time_read_from_file > 300):
        print("Device Stopped")
        #change time_read_from_file to date/time
        time_read_from_file = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_read_from_file))
        #change current_time to date/time
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
        status = "Pi was turned off from " + str(time_read_from_file) + " to " + str(current_time)
        log_sent(device_id, status)

    #read is_cached.txt file
    with open("/home/pi/Person-Detection/yolov5/is_cached.txt", "r") as f:
        is_cached =  f.read()
        #change True in string to boolean
        #print(is_cached)
        if("True" in is_cached):
            print("Cache hai")
            is_cached = True

        else:
            is_cached = False
    if(is_cached == True):
        print("Connectivity Issue")
        if(type(time_read_from_file) == float):
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
        status = "Pi Connectivity was disrupted and was resumed at " + str(current_time)
        log_sent(device_id, status)



if __name__ == "__main__":
    log_data("1")

    
