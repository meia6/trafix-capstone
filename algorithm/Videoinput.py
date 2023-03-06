import Intersection
import TrafficLight
import time
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import urllib.request
import numpy as np
from cvlib.object_detection import draw_bbox
import concurrent.futures
import Videoinput
def video_input(video_file):
    
    cap = cv2.VideoCapture(video_file)
    count=0
    allobjects = []
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('frame{:d}.jpg'.format(count), frame)
        count += 30
        cap.set(cv2.CAP_PROP_POS_FRAMES, count)
    else:
        cap.release()
        
    bbox, label, conf = cv.detect_common_objects(frame)
    frame = draw_bbox(frame, bbox, label, conf)
    for l in label:
        allobjects.append(l)

    for i in allobjects:
        count+=1
        print(f"Detected object: {i}\n")

    with open('car_count.txt', 'w') as f:
        f.write(str(count))

    cv2.imshow('detection',frame)
    return count
