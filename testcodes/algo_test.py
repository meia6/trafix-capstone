import time
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import urllib.request
import numpy as np
from cvlib.object_detection import draw_bbox
import concurrent.futures
import math
#import VideoInput
# Main driver file

#Initializing
program_running = True
intersections = []
selector=0
runtime=0
prevlight_runtime=0
video_frame_count=0
max_time= False
light_time_length=[5,10,15,20,25,0]#time selects (0 mins at the end is for initial case.)
min_time_light= [5,10,15,20,25,0]
max_time_light= [5,10,15,20,25,0]
prev_time_selector=5
traffic_light_NS = "green"
traffic_light_EW = "red"
while(program_running):
    
    #video_frame_count,camera_count_N=VideoInput.video_input('traffic1.mp4',video_frame_count)
    #print(video_frame_count)
    #print(camera_count_N)
    camera_count_N = 5
    camera_count_E = 2
    camera_count_S = 5
    camera_count_W = 2
    runtime+=1
    time.sleep(0.2)
    print(runtime)
    camera_counts = [camera_count_N,camera_count_E,camera_count_S,camera_count_W]
    #for i in range(len(intersection.traffic_lights)):  # scan file to get traffic count for all 4 cameras. Index 0 and 2, 1 and 3 are opposite of each other
    #    traffic_data = open("%s.txt" % intersection.traffic_lights[i].get_camera, "r")  # contains the number of cars detected in each camera
    #    camera_counts[i] = traffic_data.read() 
    #    #timing is polling-based. This is done according to how often we sample the camera car counts.

    #threshold is the # of cars in the direction that will be a problem to us (# of cars that is considered as traffic)
    #speed_limit
    threshold_NS=4
    threshold_EW=2
    ratio_NS = (camera_counts[0] + camera_counts[2]) / threshold_NS #ex. if ratio=1, base traffic congestion. call light_time_length[1].
    ratio_EW = (camera_counts[1] + camera_counts[3]) / threshold_EW #if ratio=2, 2nd level of traffic congestion. call light_time_length[2].
    #if statement to decide congestion level (might be redundant based on ratio_NS>ratio_EW nested if statement)
    if ratio_NS > ratio_EW:
        time_selector=math.ceil(ratio_NS)
    else:
        time_selector=math.ceil(ratio_EW)

    #if statement to check what congestion response is needed
    if time_selector==0:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if ratio_NS>ratio_EW:
                    #switching to other light
                    traffic_light_EW="green"
                    traffic_light_NS="red"
                    prevlight_runtime=runtime
                    prev_time_selector=time_selector
                    light_time_length[time_selector] #call this extra?
                    max_time=False
                    #send state of light for NS: red=0
                    #send camera 
                    print("hi0 max")
                else:
                    #switching to other light
                    traffic_light_NS="green"
                    traffic_light_NS="red"
                    prevlight_runtime=runtime
                    prev_time_selector=time_selector
                    light_time_length[time_selector] #call this extra?
                    max_time=False
            else:
                #send # of car 
                pass
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=time_selector
                        light_time_length[time_selector] #call this extra?
                        max_time=True
                        print("hi0")
                         
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        prev_time_selector=time_selector
                        light_time_length[time_selector]
                        max_time=False
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=time_selector
                        light_time_length[time_selector] #call this extra?
                        max_time=True
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        prev_time_selector=time_selector
                        light_time_length[time_selector]
                        max_time=False
            else:
                pass
    elif time_selector==1:
       #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if ratio_NS>ratio_EW:
                    #switching to other light
                    traffic_light_EW="green"
                    traffic_light_NS="red"
                    prevlight_runtime=runtime
                    prev_time_selector=time_selector
                    light_time_length[time_selector] #call this extra?
                    max_time=False
                    #send state of light for NS: red=0
                    #send camera 
                    print("hi1 max")
                else:
                    #switching to other light
                    traffic_light_NS="green"
                    traffic_light_NS="red"
                    prevlight_runtime=runtime
                    prev_time_selector=time_selector
                    light_time_length[time_selector] #call this extra?
                    max_time=False
            else:
                #send # of car 
                pass
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=time_selector
                        light_time_length[time_selector] #call this extra?
                        max_time=True
                        print("hi1")
                         
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        prev_time_selector=time_selector
                        light_time_length[time_selector]
                        max_time=False
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=time_selector
                        light_time_length[time_selector] #call this extra?
                        max_time=True
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        prev_time_selector=time_selector
                        light_time_length[time_selector]
                        max_time=False
            else:
                pass
    elif time_selector==2:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if ratio_NS>ratio_EW:
                    #switching to other light
                    traffic_light_EW="green"
                    traffic_light_NS="red"
                    prevlight_runtime=runtime
                    prev_time_selector=time_selector
                    light_time_length[time_selector] #call this extra?
                    max_time=False
                    #send state of light for NS: red=0
                    #send camera 
                    print("hi2 max")
                else:
                    #switching to other light
                    traffic_light_NS="green"
                    traffic_light_NS="red"
                    prevlight_runtime=runtime
                    prev_time_selector=time_selector
                    light_time_length[time_selector] #call this extra?
                    max_time=False
            else:
                #send # of car 
                pass
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=time_selector
                        light_time_length[time_selector] #call this extra?
                        max_time=True
                        print("hi2")
                         
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        prev_time_selector=time_selector
                        light_time_length[time_selector]
                        max_time=False
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=time_selector
                        light_time_length[time_selector] #call this extra?
                        max_time=True
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        prev_time_selector=time_selector
                        light_time_length[time_selector]
                        max_time=False
            else:
                pass
    elif time_selector==3:
       #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if ratio_NS>ratio_EW:
                    #switching to other light
                    traffic_light_EW="green"
                    traffic_light_NS="red"
                    prevlight_runtime=runtime
                    prev_time_selector=time_selector
                    light_time_length[time_selector] #call this extra?
                    max_time=False
                    #send state of light for NS: red=0
                    #send camera 
                    print("hi3 max NS OFF")
                else:
                    #switching to other light
                    traffic_light_NS="green"
                    traffic_light_EW="red"
                    prevlight_runtime=runtime
                    prev_time_selector=time_selector
                    light_time_length[time_selector] #call this extra?
                    max_time=False
                    print("hi3 max NS ON")
            else:
                #send # of car 
                pass
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=time_selector
                        light_time_length[time_selector] #call this extra?
                        max_time=True
                        print("hi3 NS STAY ON")
                         
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        traffic_light_NS="green"
                        traffic_light_EW="red"
                        prev_time_selector=time_selector
                        light_time_length[time_selector]
                        max_time=False
                        print("hi3 EW OFF (NS ON)")
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=time_selector
                        light_time_length[time_selector] #call this extra?
                        max_time=True
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        traffic_light_NS=="red"
                        traffic_light_EW=="green"
                        prev_time_selector=time_selector
                        light_time_length[time_selector]
                        max_time=False
            else:
                pass
    elif time_selector==4:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if ratio_NS>ratio_EW:
                    #switching to other light
                    traffic_light_EW="green"
                    traffic_light_NS="red"
                    prevlight_runtime=runtime
                    prev_time_selector=time_selector
                    light_time_length[time_selector] #call this extra?
                    max_time=False
                    #send state of light for NS: red=0
                    #send camera 
                    print("hi4 max")
                else:
                    #switching to other light
                    traffic_light_NS="green"
                    traffic_light_NS="red"
                    prevlight_runtime=runtime
                    prev_time_selector=time_selector
                    light_time_length[time_selector] #call this extra?
                    max_time=False
            else:
                #send # of car 
                pass
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=time_selector
                        light_time_length[time_selector] #call this extra?
                        max_time=True
                        print("hi4")
                         
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        prev_time_selector=time_selector
                        light_time_length[time_selector]
                        max_time=False
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=time_selector
                        light_time_length[time_selector] #call this extra?
                        max_time=True
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        prev_time_selector=time_selector
                        light_time_length[time_selector]
                        max_time=False
            else:
                pass