import func_timeout
from requests import request
import os
def long_function(time_t):
    while(time_t < 10):
        print("Two rupees pepsi Harsh is Sexy")
        time_t+=1


    return time_t

def run_function(f, max_wait, default_value):
    try:
        return func_timeout.func_timeout(max_wait, long_function, args=[1])
    except func_timeout.FunctionTimedOut:
        pass
    return default_value


x = run_function(long_function, 5, 'world')
print(x)



def send_video():
    file_path = os.path.join('./', "person.mp4")
    device_id = 32
    url = "http://as99.zvastica.solutions/appapi/submitviolence"
    #payload = {'device_id': '1234'
    #device_id = device_id.replace("\"", "")
    payload = {'device_id': device_id}
    #payload = "{\'device_id\': " + device_id + "00" + "}"
    print(payload)
    files = [
    ('file', open( file_path ,'rb'))
    ]
    headers = {
    'Cookie': 'ci_session=sn7n11lsss9vdlrej79sq6s1o0c5mm3r'
    }
    response = request("POST", url, headers=headers, data = payload, files = files)
    response  = response.text.encode('utf8')
    print(response)
    return response
#print(response.text.encode('utf8'))

def run_function_2(f, max_wait, default_value):
    try:
        #response = request("POST", url, headers=headers, data = payload, files = files)
        return func_timeout.func_timeout(max_wait, send_video)
    except func_timeout.FunctionTimedOut:
        pass
    return default_value


x = run_function_2(long_function, 5, 'world')
print(x)