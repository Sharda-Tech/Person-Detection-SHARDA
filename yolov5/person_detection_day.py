import cv2
import numpy as np
import os
from elements.yolo import OBJ_DETECTION
from email_sender import send_email
import requests
import time
from pyembedded.raspberry_pi_tools.raspberrypi import PI
pi = PI()
from check_internet_connectivity import is_connected
from sent_status_every_12_hours import check_if_12_hours
from logger import log_data
from sound import play_sound


def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial


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
            with open('/home/pi/Person-Detection/yolov5/device_id.txt', 'w') as f:
                f.write(device_id)
                f.close()
            return "Device id written to file"


def request_status(device_id):
  url = "http://as99.zvastica.solutions/appapi/checkdevicestatusbyhw"

  #payload = "{\n    \"device_id\":\"2\"\n }"
  payload = "{ \n \n \"device_id\" : " + device_id + " \n \n \n}"
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data = payload)

  #print(response.text.encode('utf8'))

  #convert byte to string

  print(response.text)

  #split string using ','

  str = response.text.split(',')

  #print(str[1])

  status = str[1].split(':')

  #print(status[1])

  return status[1]

def write_log(detection):
    with open('/home/pi/Person-Detection/yolov5/log.txt', 'a') as f:
        #write the date and time
        f.write(time.strftime("%d/%m/%Y %H:%M:%S"))
        f.write('\n')
        f.write("Number of Detection: " +  str(detection))
        f.write('\n')
        f.write('Cpu Usage is' +  str(pi.get_cpu_usage()))
        f.write('\n')
        f.write('Memory Usage is ' + str( pi.get_ram_info()))
        f.write('\n')
        f.write('CPU temperature is ' +  str(pi.get_cpu_temp()))
        f.write('\n')

def sent_video(device_id):

    for file in os.listdir('/home/pi/Person-Detection/yolov5//output'):

        file_path = os.path.join('/home/pi/Person-Detection/yolov5//output', file)

        url = "http://as99.zvastica.solutions/appapi/submitviolence"
        #payload = {'device_id': '1234'
        device_id = device_id.replace("\"", "")
        payload = {'device_id': device_id}
        #payload = "{\'device_id\': " + device_id + "00" + "}"
        print(payload)
        files = [
        ('file', open( file_path ,'rb'))
        ]
        headers = {
        'Cookie': 'ci_session=sn7n11lsss9vdlrej79sq6s1o0c5mm3r'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)

        print(response.text.encode('utf8'))


    #remove contents of output folder
    for file in os.listdir('/home/pi/Person-Detection/yolov5//output'):
        file_path = os.path.join('/home/pi/Person-Detection/yolov5//output', file)
        os.remove(file_path)
    

    return True

def predict():

    prev_time = 0
    new_time = time.time()
    record_time = time.time()

    video_sent_status = False
    number_of_person_detected = 0
    previous_number_of_person_detected = {}
    previous_number_of_person_detected = {'Number' : 0 , 'Time' : time.time()}
    meta_of_number_of_person_detected = {'Number' : 0 , 'frame_number' : 0 , 'number_of_frames_not_detected' : 0}
    frames_counter = 0
    frames = []
    not_detected_frames_thresh = 10
    number_of_frames_not_detected = 0



    #if is_cache does not exist, create it
    if not os.path.exists('/home/pi/Person-Detection/yolov5/is_cache.txt'):
        with open('/home/pi/Person-Detection/yolov5/is_cache.txt', 'w') as f:
            f.write('')
            f.close()
    
    #read is_cached from file
    with open('/home/pi/Person-Detection/yolov5//is_cached.txt', 'r') as f:
        is_cached = f.read()
        #print(type(bool(is_cached)))
        if("True" in is_cached):
            is_cached = True

        else:
            is_cached = False
        f.close()


    if is_cached == '':
        is_cached = False
        #write is_cached to file
        with open('/home/pi/Person-Detection/yolov5//is_cached.txt', 'w') as f:
            f.write(str(is_cached))
            f.close()

    
    Object_classes = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
                    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
                    'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
                    'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
                    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
                    'hair drier', 'toothbrush' ]

    #Object_colors = list(np.random.rand(80,3)*255)
    Object_detector = OBJ_DETECTION('/home/pi/Person-Detection/yolov5/yolov5n-int8.tflite', Object_classes)
    # Return true if line segments AB and CD intersect
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    #print(gstreamer_pipeline(flip_method=0))
    #cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    cap = cv2.VideoCapture(0)
    serial = getserial()
    REMOTE_SERVER = "www.google.com"
    if is_connected(REMOTE_SERVER):
        registration_status = register(serial)
        
    else:
        registration_status = "Device id written to file"
        
    if(registration_status == "Device id written to file"):
        #read the device id from the text file
        with open('/home/pi/Person-Detection/yolov5/device_id.txt', 'r') as f:
            device_id = f.read()
            f.close()

    if(prev_time == 0):

        # status_of_device = request_status(device_id)
        # #status_of_device = 'false'

        if is_connected(REMOTE_SERVER):
                try:
                    y = request_status(device_id)

                except:
                    y = 'false'

                status_of_device = y

        else:

            status_of_device = 'false'

        prev_time = new_time
        new_time = time.time()


    while cap.isOpened():
        
        REMOTE_SERVER = "www.google.com"
        if is_connected(REMOTE_SERVER):
            print("connected")
            cache = False
            with open('/home/pi/Person-Detection/yolov5//is_cache.txt','w') as f:
                f.write(str(cache))
                f.close
            try:

                log_data(device_id)
                check_if_12_hours(device_id)

            except:

                pass
        
            if( is_cached == True):
                print("Cached")
                print(device_id)
                sent_video(device_id)
                is_cached = False
                #write is_cached to file
                with open('/home/pi/Person-Detection/yolov5//is_cached.txt', 'w') as f:
                    f.write(str(is_cached))
                    f.close()


        else:
            print("not connected")
            cache = True
            with open('/home/pi/Person-Detection/yolov5//is_cache.txt', 'w') as f:
                f.write(str(cache))
                f.close()
        
        #window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # Window
        #while cv2.getWindowProperty("CSI Camera", 0) >= 0 :
        ret, frame = cap.read()
        new_time = time.time()
        #print("Previous Time", prev_time)
        #print("New Time", new_time)

        if((new_time - prev_time) >= 4):
            if is_connected(REMOTE_SERVER):
                original_status = status_of_device
                try:
                    y = request_status(device_id)

                except:
                    y = original_status

                status_of_device = y
            print(status_of_device)
            #status_of_device = 'true'

            prev_time = new_time
            new_time = time.time()

        if ret and status_of_device == 'true':
            # detection process
            objs = Object_detector.detect(frame)
            dets = []
            # plotting
            
            number_of_person_detected = 0

            for obj in objs:
                # print(obj)
                label = obj['label']
                if((label == 'person')):
                    number_of_frames_not_detected = 0
                    number_of_person_detected +=1
                    #print(label)
                    score = obj['score']
                    [(xmin,ymin),(xmax,ymax)] = obj['bbox']
                    #print(xmin,ymin,xmax,ymax)
                    (x, y) = (xmin, ymin)
                    (w, h) = ((xmax-xmin),(ymax-ymin))
                    #color = Object_colors[Object_classes.index(label)]
                    frame = cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (255,0,0), 2) 
                    frame = cv2.putText(frame, f'{label} ({str(score)})', (xmin,ymin), cv2.FONT_HERSHEY_SIMPLEX , 0.75, (0,255,255), 1, cv2.LINE_AA)


                



            
            if(number_of_person_detected > meta_of_number_of_person_detected['Number'] or number_of_person_detected < meta_of_number_of_person_detected['Number']):
                if(number_of_person_detected == 0):
                    meta_of_number_of_person_detected['number_of_frames_not_detected'] +=1

                    if(meta_of_number_of_person_detected['number_of_frames_not_detected'] > not_detected_frames_thresh):
                        meta_of_number_of_person_detected['Number'] = number_of_person_detected
                
                        meta_of_number_of_person_detected['frame_number'] = 1
                if(number_of_person_detected > 0):
                    meta_of_number_of_person_detected['number_of_frames_not_detected'] = 0
                    meta_of_number_of_person_detected['Number'] = number_of_person_detected
                    meta_of_number_of_person_detected['frame_number'] +=1

            if(number_of_person_detected == meta_of_number_of_person_detected['Number']):
                meta_of_number_of_person_detected['frame_number'] += 1
            
            print("Frames Counter", frames_counter)
            print("Number of person detected:", meta_of_number_of_person_detected, "Previous number of person detected:", previous_number_of_person_detected)
            if((meta_of_number_of_person_detected['Number'] > previous_number_of_person_detected['Number']) and meta_of_number_of_person_detected['frame_number'] > 10):
                print("New Person Detected")
                previous_number_of_person_detected['Number'] = meta_of_number_of_person_detected['Number']
                #previous_number_of_person_detected['Time'] = number_of_person_detected['Time']
                if(video_sent_status == True):
                    video_sent_status = False
                    frames_counter = 0


            elif((meta_of_number_of_person_detected['Number'] < previous_number_of_person_detected['Number']) and meta_of_number_of_person_detected['frame_number'] > 10):
                print("Person Detected Reduced")
                previous_number_of_person_detected['Number'] = meta_of_number_of_person_detected['Number']
                #previous_number_of_person_detected['Time'] = number_of_person_detected['Time']
                if(video_sent_status == True):
                    video_sent_status = False
                    frames_counter = 0


            if(video_sent_status == False and previous_number_of_person_detected['Number'] > 0):
                if(frames_counter == 30):
                    #play sound
                    play_sound(40)
                if(frames_counter < 31):
                    frames_counter = frames_counter + 1
                    frames.append(frame)
                elif(frames_counter == 31):
                    frames_counter = frames_counter + 1
                    REMOTE_SERVER = "www.google.com"
                    if is_connected(REMOTE_SERVER):
                        print("connected")
                        cache = False
                        with open('/home/pi/Person-Detection/yolov5//is_cache.txt', 'w') as f:
                            f.write(str(cache))
                            f.close()

                    else:
                        print("not connected")
                        cache = True
                        with open('/home/pi/Person-Detection/yolov5//is_cache.txt', 'w') as f:
                            f.write(str(cache))
                            f.close()
                    if(cache == False):
                        #write a list of frames in a video
                        current_file_number = 0
                        output_file_save_name = '/home/pi/Person-Detection/yolov5/output/output_' + str(current_file_number) + '.mp4'
                        out = cv2.VideoWriter(output_file_save_name,cv2.VideoWriter_fourcc(*'avc1'), 10, (frame.shape[1],frame.shape[0]))
                        for i in range(len(frames)):
                            out.write(frames[i])
                        out.release()
                        print(device_id)
                        video_sent_status = sent_video(device_id)
                        if video_sent_status == True:
                            print("Video sent")
                        frames = []

                    if(cache == True):
                        current_file_number = 0
                        #find the folders in the cache folder
                        for file in os.listdir('/home/pi/Person-Detection/yolov5/output'):
                            if file.endswith(".mp4"):
                                file_number = file.split("_")[1]
                                file_number = file_number.split(".")[0]

                                if(int(file_number) > current_file_number):
                                    current_file_number = int(file_number)

                        output_file_save_name = "/home/pi/Person-Detection/yolov5/output/output_" + str(current_file_number + 1) + ".mp4"
                        out = cv2.VideoWriter(output_file_save_name,cv2.VideoWriter_fourcc(*'avc1'), 10, (frame.shape[1],frame.shape[0]))
                        for i in range(len(frames)):
                            out.write(frames[i])
                        out.release()
                        print(device_id)
                        is_cached = True
                        #write is_cached to a file
                        with open('/home/pi/Person-Detection/yolov5/is_cached.txt', 'w') as f:
                            f.write(str(is_cached))
                        frames = []


            print("Number of Frames not detected" , number_of_frames_not_detected)
            if(number_of_frames_not_detected < not_detected_frames_thresh and number_of_person_detected == 0):
                    number_of_frames_not_detected = number_of_frames_not_detected + 1
            elif(number_of_frames_not_detected >= not_detected_frames_thresh and number_of_person_detected == 0):
                    video_sent_status = False
                    if(frames_counter >= 10):
                        frames_counter = frames_counter + 1
                        REMOTE_SERVER = "www.google.com"
                        if is_connected(REMOTE_SERVER):
                            print("connected")
                            cache = False
                            with open('/home/pi/Person-Detection/yolov5/is_cache.txt', 'w') as f:
                                f.write(str(cache))
                                f.close()

                        else:
                            print("not connected")
                            cache = True
                            with open('/home/pi/Person-Detection/yolov5/is_cache.txt', 'w') as f:
                                f.write(str(cache))
                                f.close()
                        if(cache == False):
                            #write a list of frames in a video
                            current_file_number = 0
                            output_file_save_name = '/home/pi/Person-Detection/yolov5/output/output_' + str(current_file_number) + '.mp4'
                            out = cv2.VideoWriter(output_file_save_name,cv2.VideoWriter_fourcc(*'avc1'), 10, (frame.shape[1],frame.shape[0]))
                            for i in range(len(frames)):
                                out.write(frames[i])
                            out.release()
                            print(device_id)
                            video_sent_status = sent_video(device_id)
                            if video_sent_status == True:
                                print("Video sent")
                            frames = []

                        if(cache == True):
                            current_file_number = 0
                            #find the folders in the cache folder
                            for file in os.listdir('/home/pi/Person-Detection/yolov5/output'):
                                if file.endswith(".mp4"):
                                    file_number = file.split("_")[1]
                                    file_number = file_number.split(".")[0]

                                    if(int(file_number) > current_file_number):
                                        current_file_number = int(file_number)

                            output_file_save_name = "/home/pi/Person-Detection/yolov5/output/output_" + str(current_file_number + 1) + ".mp4"
                            out = cv2.VideoWriter(output_file_save_name,cv2.VideoWriter_fourcc(*'avc1'), 10, (frame.shape[1],frame.shape[0]))
                            for i in range(len(frames)):
                                out.write(frames[i])
                            out.release()
                            print(device_id)
                            is_cached = True
                            #write is_cached to a file
                            with open('/home/pi/Person-Detection/yolov5/is_cached.txt', 'w') as f:
                                f.write(str(is_cached))
                            
                    frames_counter = 0
                    frames = []
                    number_of_person_detected = 0
                    previous_number_of_person_detected['Number'] = 0


        if(time.time() - record_time >= 1):
            record_time = time.time()
            write_log(number_of_person_detected)

        #cv2.imshow("CSI Camera", frame)
        #keyCode = cv2.waitKey(30)
        #if keyCode == ord('q'):
                #break      
    #cap.release()
    #cv2.destroyAllWindows()



if __name__ == "__main__":
    predict()
