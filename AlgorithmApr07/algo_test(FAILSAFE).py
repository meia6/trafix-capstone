import time
import serial
from struct import *
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import urllib.request
import numpy as np
from cvlib.object_detection import draw_bbox
import concurrent.futures
import math
import random
import VideoInput
# Main driver file

#Initializing
program_running = True
intersections = []
selector=0
runtime=0
prevlight_runtime=0
video_frame_count=52
max_time= False
light_time_length=[5,10,15,20,25,30,0]#time selects (0 mins at the end is for initial case.)
min_time_light= [5,10,15,20,25,30,0]
max_time_light= [5,5,5,5,5,5,0]
prev_time_selector=6
traffic_light_NS = "green"
traffic_light_EW = "red"
lightstate=1

try:
    ser=serial.Serial(baudrate='115200', timeout=1, port='com8')    #!!!
except:
    print('Port open error')
    
while(program_running):
    
    video_frame_count,camera_count_N=VideoInput.video_input('Trafix_Camera1.mp4',video_frame_count)
    video_frame_count,camera_count_E=VideoInput.video_input('Trafix_Camera2.mp4',video_frame_count)
    video_frame_count,camera_count_S=VideoInput.video_input('Trafix_Camera3.mp4',video_frame_count)
    video_frame_count,camera_count_W=VideoInput.video_input('Trafix_Camera4.mp4',video_frame_count)
    print("frame count:",video_frame_count)
    print("Ncar count:", camera_count_N)
    print("Ecar count:", camera_count_E)
    print("Scar count:", camera_count_S)
    print("Wcar count:", camera_count_W)
    if camera_count_E > 6:
        camera_count_E = 6

    if camera_count_W > 6:
        camera_count_W = 6
    
    #camera_count_N = random.randint(1,12)
    #camera_count_E = random.randint(1,6)
    #camera_count_S = random.randint(1,12)
    #camera_count_W = random.randint(1,6)
    runtime+=1
    time.sleep(2)
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
    if (time_selector-1)==0:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if ratio_NS>ratio_EW:
                    #switching to other light
                    traffic_light_EW="green"
                    lightstate=0
                    traffic_light_NS="red"

                    #set previous variables to current, resetting conditionals for next switching case
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    max_time=False
                    
                    #send state of light for NS: red=0
                    #send camera 
                    ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                    print("time 0 max NS OFF (EW ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    #switching to other light
                    traffic_light_NS="green"
                    lightstate=1
                    traffic_light_EW="red"
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                    max_time=False
                    print("time 0 max EW OFF (NS ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":
                    light_advance = math.ceil(ratio_NS)-1
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
                elif traffic_light_EW == "green":
                    light_advance = math.ceil(ratio_EW)-1
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=True
                        print("time 0 NS STAY ON")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        traffic_light_NS="green"
                        lightstate=1
                        traffic_light_EW="red"
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=False
                        print("time 0 NS ON (EW OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=True
                        print("time 0 EW STAY ON")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                    else:
                        prevlight_runtime=runtime
                        #switch lights from red
                        traffic_light_NS="red"
                        traffic_light_EW="green"
                        lightstate=0
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=False
                        print("time 0 EW ON (NS OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":
                    light_advance = math.ceil(ratio_NS)-1
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
                elif traffic_light_EW == "green":
                    light_advance = math.ceil(ratio_EW)-1
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
    elif (time_selector-1)==1:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if ratio_NS>ratio_EW:
                    #switching to other light
                    traffic_light_EW="green"
                    lightstate=0
                    traffic_light_NS="red"

                    #set previous variables to current, resetting conditionals for next switching case
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    max_time=False
                    
                    #send state of light for NS: red=0
                    #send camera 
                    ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                    print("time 1 max NS OFF (EW ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    #switching to other light
                    traffic_light_NS="green"
                    lightstate=1
                    traffic_light_EW="red"
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                    max_time=False
                    print("time 1 max EW OFF (NS ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":
                    light_advance = math.ceil(ratio_NS)-1
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
                elif traffic_light_EW == "green":
                    light_advance = math.ceil(ratio_EW)-1
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=True
                        print("time 1 NS STAY ON")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        traffic_light_NS="green"
                        lightstate=1
                        traffic_light_EW="red"
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=False
                        print("time 1 NS ON (EW OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=True
                        print("time 1 EW STAY ON")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                    else:
                        prevlight_runtime=runtime
                        #switch lights from red
                        traffic_light_NS="red"
                        traffic_light_EW="green"
                        lightstate=0
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=False
                        print("time 1 EW ON (NS OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":
                    light_advance = math.ceil(ratio_NS)-1
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
                elif traffic_light_EW == "green":
                    light_advance = math.ceil(ratio_EW)-1
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
    elif (time_selector-1)==2:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if ratio_NS>ratio_EW:
                    #switching to other light
                    traffic_light_EW="green"
                    lightstate=0
                    traffic_light_NS="red"

                    #set previous variables to current, resetting conditionals for next switching case
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    max_time=False
                    
                    #send state of light for NS: red=0
                    #send camera 
                    ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                    #serial.write(pack(car_count_N,car_count_E,car_count_S,car_count_W,traffic_light_NS)
                    print("time 2 max NS OFF (EW ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    #switching to other light
                    traffic_light_NS="green"
                    lightstate=1
                    traffic_light_EW="red"
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                    max_time=False
                    print("time 2 max EW OFF (NS ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":
                    light_advance = math.ceil(ratio_NS)-1
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
                elif traffic_light_EW == "green":
                    light_advance = math.ceil(ratio_EW)-1
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=True
                        print("time 2 NS STAY ON")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        traffic_light_NS="green"
                        lightstate=1
                        traffic_light_EW="red"
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=False
                        print("time 2 NS ON (EW OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=True
                        print("time 2 EW STAY ON")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                    else:
                        prevlight_runtime=runtime
                        #switch lights from red
                        traffic_light_NS="red"
                        traffic_light_EW="green"
                        lightstate=0
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=False
                        print("time 2 EW ON (NS OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":
                    light_advance = math.ceil(ratio_NS)-1
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
                elif traffic_light_EW == "green":
                    light_advance = math.ceil(ratio_EW)-1
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
    elif (time_selector-1)==3:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if ratio_NS>ratio_EW:
                    #switching to other light
                    traffic_light_EW="green"
                    lightstate=0
                    traffic_light_NS="red"
                    
                    #set previous variables to current, resetting conditionals for next switching case
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    max_time=False
                    
                    #send state of light for NS: red=0
                    #send camera 
                    ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                    #serial.write(pack(car_count_N,car_count_E,car_count_S,car_count_W,traffic_light_NS)
                    print("time 3 max NS OFF (EW ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    #switching to other light
                    traffic_light_NS="green"
                    lightstate=1
                    traffic_light_EW="red"
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                    max_time=False
                    print("time 3 max EW OFF (NS ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":
                    light_advance = math.ceil(ratio_NS)-1
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
                elif traffic_light_EW == "green":
                    light_advance = math.ceil(ratio_EW)-1
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=True
                        print("time 3 NS STAY ON")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        traffic_light_NS="green"
                        lightstate=1
                        traffic_light_EW="red"
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=False
                        print("time 3 NS ON (EW OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=True
                        print("time 3 EW STAY ON")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                    else:
                        prevlight_runtime=runtime
                        #switch lights from red
                        traffic_light_NS="red"
                        traffic_light_EW="green"
                        lightstate=0
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=False
                        print("time 3 EW ON (NS OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":
                    light_advance = math.ceil(ratio_NS)-1
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
                elif traffic_light_EW == "green":
                    light_advance = math.ceil(ratio_EW)-1
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
    elif (time_selector-1)==4:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if ratio_NS>ratio_EW:
                    #switching to other light
                    traffic_light_EW="green"
                    lightstate=0
                    traffic_light_NS="red"

                    #set previous variables to current, resetting conditionals for next switching case
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    max_time=False
                    
                    #send state of light for NS: red=0
                    #send camera 
                    ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                    #serial.write(pack(car_count_N,car_count_E,car_count_S,car_count_W,traffic_light_NS)
                    print("time 4 max NS OFF (EW ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    #switching to other light
                    traffic_light_NS="green"
                    lightstate=1
                    traffic_light_EW="red"
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                    max_time=False
                    print("time 4 max EW OFF (NS ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":
                    light_advance = math.ceil(ratio_NS)-1
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
                elif traffic_light_EW == "green":
                    light_advance = math.ceil(ratio_EW)-1
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=True
                        print("time 4 NS STAY ON")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        traffic_light_NS="green"
                        lightstate=1
                        traffic_light_EW="red"
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=False
                        print("time 4 NS ON (EW OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=True
                        print("time 4 EW STAY ON")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                    else:
                        prevlight_runtime=runtime
                        #switch lights from red
                        traffic_light_NS="red"
                        traffic_light_EW="green"
                        lightstate=0
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=False
                        print("time 4 EW ON (NS OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":
                    light_advance = math.ceil(ratio_NS)-1
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
                elif traffic_light_EW == "green":
                    light_advance = math.ceil(ratio_EW)-1
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
    elif (time_selector-1)==5:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if ratio_NS>ratio_EW:
                    #switching to other light
                    traffic_light_EW="green"
                    lightstate=0
                    traffic_light_NS="red"

                    #set previous variables to current, resetting conditionals for next switching case
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    max_time=False
                    
                    #send state of light for NS: red=0
                    #send camera 
                    ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                    #serial.write(pack(car_count_N,car_count_E,car_count_S,car_count_W,traffic_light_NS)
                    print("time 5 max NS OFF (EW ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    #switching to other light
                    traffic_light_NS="green"
                    lightstate=1
                    traffic_light_EW="red"
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                    max_time=False
                    print("time 5 max EW OFF (NS ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":
                    light_advance = math.ceil(ratio_NS)-1
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
                elif traffic_light_EW == "green":
                    light_advance = math.ceil(ratio_EW)-1
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=True
                        print("time 5 NS STAY ON")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                    else:
                        prevlight_runtime=runtime
                        #switch lights to red
                        traffic_light_NS="green"
                        lightstate=1
                        traffic_light_EW="red"
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=False
                        print("time 5 NS ON (EW OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=True
                        print("time 5 EW STAY ON")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                    else:
                        prevlight_runtime=runtime
                        #switch lights from red
                        traffic_light_NS="red"
                        traffic_light_EW="green"
                        lightstate=0
                        prev_time_selector=(time_selector-1)
                        ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_time=False
                        print("time 5 EW ON (NS OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                ser.write(pack('5h',camera_count_S,camera_count_N,camera_count_E,camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":
                    light_advance = math.ceil(ratio_NS)-1
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
                elif traffic_light_EW == "green":
                    light_advance = math.ceil(ratio_EW)-1
                    if prev_time_selector - light_advance==0:
                        pass
                    elif prev_time_selector - light_advance==1:
                        runtime +=1
                    elif prev_time_selector - light_advance==2:
                        runtime +=2
                    elif prev_time_selector - light_advance==3:
                        runtime +=3
                    elif prev_time_selector - light_advance==4:
                        runtime +=4
                    elif prev_time_selector - light_advance==5:
                        runtime +=5
                    elif prev_time_selector - light_advance==6:
                        runtime +=6
