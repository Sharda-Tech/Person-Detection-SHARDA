import cv2
import numpy as np
from elements.yolo import OBJ_DETECTION
from sort import *
from email_sender import send_email

def intersect(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def ccw(A,B,C):
	return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

#equation of a line:
def line_eq(A,B):
    m = (B[1]-A[1])/(B[0]-A[0])
    b = A[1] - m*A[0]
    return m,b

def intersect_2(point,m,b):
    print("Y Predicted", m*point[0]+b)
    print("Y Real is", point[1])
    if(point[1] > m*point[0]+b) and (point[1] < m*point[0]+b+1):
        return True


def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def predict():
    memory = {}
    line = [(140,270),(180,280)]
    counter = 0
    import time
    prev_time = 0
    new_time = 0
    frames = []
    tracker = Sort()
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
    Object_detector = OBJ_DETECTION('./yolov5n-fp16.tflite', Object_classes)
    prev_time = 0
    new_time = 0
    m,b = line_eq(line[0],line[1])
    recorded_time = 0
    start_time = time.time()
    metadata = np.array([])
    fresh_start = True
    time_duration = 20 #in seconds
    # Return true if line segments AB and CD intersect
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    #cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    cap = cv2.VideoCapture('./hj.mp4')
    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # Window
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            ret, frame = cap.read()
            if ret:
                recorded_time = time.time()
                metadata = [recorded_time, counter]
                if(fresh_start is True):
                    if 'metadata_tipper.npy' in os.listdir('./metadata'):
                        metadata = np.load('./metadata/metadata_tipper.npy')
                        recorded_time = metadata[0]
                        counter  = metadata[1]
                        #remove metadata.npy file
                        os.remove('./metadata/metadata_tipper.npy')
                    fresh_start = False
                if(recorded_time - start_time > time_duration):
                    start_time = recorded_time
                    message = "Count for Tipper: " + str(metadata[1])
                    counter = 0
                    send_email(message)

                    
                # save a numpy array to disk
                np.save('./metadata/metadata_tipper.npy', metadata)
                # detection process
                objs = Object_detector.detect(frame)
                dets = []
                # plotting
                for obj in objs:
                    # print(obj)
                    label = obj['label']
                    if((label == 'truck')):
                        score = obj['score']
                        [(xmin,ymin),(xmax,ymax)] = obj['bbox']
                        #print(xmin,ymin,xmax,ymax)
                        (x, y) = (xmin, ymin)
                        (w, h) = ((xmax-xmin),(ymax-ymin))
                        dets.append([x, y, x+w, y+h, score])
                        #color = Object_colors[Object_classes.index(label)]
                        frame = cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (255,0,0), 2) 
                        #frame = cv2.putText(frame, f'{label} ({str(score)})', (xmin,ymin), cv2.FONT_HERSHEY_SIMPLEX , 0.75, (0,255,255), 1, cv2.LINE_AA)
                #list is empty
                if(len(dets) == 0):
                    dets = np.empty((0, 5))
                dets = np.asarray(dets)
                print("Dets",dets)
                tracks = tracker.update(dets)
                print("Tracks",tracks)
                boxes = []
                indexIDs = []
                c = []
                previous = memory.copy()
                memory = {}

                
                
                for track in tracks:
                
                    boxes.append([track[0], track[1], track[2], track[3]])
                    indexIDs.append(int(track[4]))
                    memory[indexIDs[-1]] = boxes[-1]
                if len(boxes) > 0:
                    i = int(0)
                    for box in boxes:
                        # extract the bounding box coordinates
                        (x, y) = (int(box[0]), int(box[1]))
                        (w, h) = (int(box[2]), int(box[3]))

                        # draw a bounding box rectangle and label on the image
                        # color = [int(c) for c in COLORS[classIDs[i]]]
                        # cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

                        color = (255,0,0)
                        #cv2.rectangle(frame, (x, y), (w, h), color, 2)

                        if indexIDs[i] in previous:
                            previous_box = previous[indexIDs[i]]
                            (x2, y2) = (int(previous_box[0]), int(previous_box[1]))
                            (w2, h2) = (int(previous_box[2]), int(previous_box[3]))
                            p0 = (int(x + (w-x)/2), int(y + (h-y)/2))
                            p1 = (int(x2 + (w2-x2)/2), int(y2 + (h2-y2)/2))
                            p3 = ((int(x), int(y+h)/2))
                            print("The Center Point is",p3)
                            cv2.line(frame, p0, p1, color, 3)
                            #cv2.circle(frame,p3,2,color=(0,0,255), thickness=-1)
                            if intersect(p0,p1, line[0], line[1]):
                            #if intersect_2(p3,m,b):
                                new_time = time.time()
                                if(new_time - prev_time > 5):
                                    counter += 1

                                #measuring time

                        text = "{}".format(indexIDs[i])
                        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        i += 1
                        prev_time = new_time

            cv2.line(frame, line[0], line[1], (0, 255, 255), 1)
            # draw counter
            cv2.putText(frame, str(counter), (100,200), cv2.FONT_HERSHEY_DUPLEX, 5.0, (0, 255, 255), 10)
            # counter += 1		    
            frames.append(frame)
            cv2.imshow("CSI Camera", frame)
            keyCode = cv2.waitKey(30)
            if keyCode == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    #write a list of frames in a video
    #out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame.shape[1],frame.shape[0]))
    #for i in range(len(frames)):
    #    out.write(frames[i])
    #out.release()

    else:
        print("Unable to open camera")


if __name__ == "__main__":
    predict()