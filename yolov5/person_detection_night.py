import cv2
import numpy as np
from elements.yolo import OBJ_DETECTION
from email_sender import send_email



def predict():
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
    Object_detector = OBJ_DETECTION('./person_detection_dark-fp16.tflite', Object_classes)
    # Return true if line segments AB and CD intersect
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    #print(gstreamer_pipeline(flip_method=0))
    #cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    cap = cv2.VideoCapture('./person.mp4')
    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # Window
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            ret, frame = cap.read()
            if ret:        
                # detection process
                objs = Object_detector.detect(frame)
                dets = []
                # plotting
                for obj in objs:
                    # print(obj)
                    label = obj['label']
                    if((label == 'person')):
                        print(label)
                        score = obj['score']
                        [(xmin,ymin),(xmax,ymax)] = obj['bbox']
                        #print(xmin,ymin,xmax,ymax)
                        (x, y) = (xmin, ymin)
                        (w, h) = ((xmax-xmin),(ymax-ymin))
                        #color = Object_colors[Object_classes.index(label)]
                        frame = cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (255,0,0), 2) 
                        frame = cv2.putText(frame, f'{label} ({str(score)})', (xmin,ymin), cv2.FONT_HERSHEY_SIMPLEX , 0.75, (0,255,255), 1, cv2.LINE_AA)
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