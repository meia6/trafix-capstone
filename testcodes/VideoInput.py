import time
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import urllib.request
import numpy as np
from cvlib.object_detection import draw_bbox
import concurrent.futures
def video_input(video_file,frame_count):
    
    cap = cv2.VideoCapture(video_file)
    count=frame_count
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
    allobjects = []
    ret, frame = cap.read()
    x=0
    if ret:
        #cv2.imwrite('frame{:d}.jpg'.format(count), frame)
        count += 30

    else:
        cap.release()
        
    bbox, label, conf = cv.detect_common_objects(frame)
    frame = draw_bbox(frame, bbox, label, conf)
    for l in label:
        allobjects.append(l)

    for i in allobjects:
       x+=1
        #print(f"Detected object: {i}\n")

    with open('car_count.txt', 'w') as f:
        f.write(str(x))

    cv2.imshow('detection',frame)
    return count,x

video_input('traffic1.mp4',210)
