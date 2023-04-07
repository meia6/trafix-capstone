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
video_frame_countN=0
video_frame_countE=0
video_frame_countS=0
video_frame_countW=0
max_time= False
light_time_length=[5,10,15,20,25,30,0]#time selects (0 mins at the end is for initial case.)
min_time_light= [5,10,15,20,25,30,0]
max_time_light= [5,5,5,5,5,5,0]
prev_time_selector=6
traffic_light_NS = "green"
traffic_light_EW = "red"
prev_light_NS = "red"
prev_light_EW = "green"
max_time = False
lightstate=1
max_camera_count_N=0
max_camera_count_S=0
max_camera_count_E=0
max_camera_count_W=0

array_counter = 0
camera_count_arrayN = [1,1,1,1,1,1,1,1,1,1,0]
camera_count_arrayE = [1,1,1,1,1,1,1,1,1,1,0]
camera_count_arrayW = [1,1,1,1,1,1,1,1,1,1,0]
camera_count_arrayS = [1,1,1,1,1,1,1,1,1,1,0]
# try:
#     ser=serial.Serial(baudrate='115200', timeout=1, port='com8')    #!!!
# except:
#     print('Port open error')
    
while(program_running):
    
    # video_frame_countN,camera_count_N=VideoInput.video_input('Trafix_Camera1.mp4',video_frame_countN)
    # video_frame_countE,camera_count_E=VideoInput.video_input('Trafix_Camera2.mp4',video_frame_countE)
    # video_frame_countS,camera_count_S=VideoInput.video_input('Trafix_Camera3.mp4',video_frame_countS)
    # video_frame_countW,camera_count_W=VideoInput.video_input('Trafix_Camera4.mp4',video_frame_countW)
    #print("frame countN:",video_frame_countN)
    #print("frame countE:",video_frame_countE)
    #print("frame countS:",video_frame_countS)
    #print("frame countW:",video_frame_countW)
    camera_count_N=camera_count_arrayN[array_counter]
    camera_count_E=camera_count_arrayE[array_counter]
    camera_count_S=camera_count_arrayS[array_counter]
    camera_count_W=camera_count_arrayW[array_counter]
    print("Ncar count:", camera_count_N)
    print("Ecar count:", camera_count_E)
    print("Scar count:", camera_count_S)
    print("Wcar count:", camera_count_W)
    if camera_count_E > 6:
        camera_count_E = 6

    if camera_count_W > 6:
        camera_count_W = 6
    
    if (traffic_light_NS == "red")&(camera_count_N>=max_camera_count_N):
        max_camera_count_N = camera_count_N
    else:
        pass

    if (traffic_light_NS == "red")&(camera_count_S>=max_camera_count_S):
        max_camera_count_S = camera_count_S
    else:
        pass

    if (traffic_light_EW == "red")&(camera_count_E>=max_camera_count_E):
        max_camera_count_E = camera_count_E
    else:
        pass

    if (traffic_light_EW == "red")&(camera_count_W>=max_camera_count_W):
        max_camera_count_W = camera_count_W
    else:
        pass


    #camera_count_N = random.randint(1,12)
    #camera_count_E = random.randint(1,6)
    #camera_count_S = random.randint(1,12)
    #camera_count_W = random.randint(1,6)
    runtime+=1
    #time.sleep(1.3)
    #time.sleep(3)
    print(runtime)
    if traffic_light_NS == "red":
        camera_counts = [max_camera_count_N,camera_count_E,max_camera_count_S,camera_count_W]
    else:
        camera_counts = [camera_count_N,max_camera_count_E,camera_count_S,max_camera_count_W]

    #threshold is the # of cars in the direction that will be a problem to us (# of cars that is considered as traffic)
    #speed_limit
    threshold_NS=4
    threshold_EW=4
    ratio_NS = (camera_counts[0] + camera_counts[2]) / threshold_NS #ex. if ratio=1, base traffic congestion. call light_time_length[1].
    ratio_EW = (camera_counts[1] + camera_counts[3]) / threshold_EW #if ratio=2, 2nd level of traffic congestion. call light_time_length[2].
    #if statement to decide congestion level (might be redundant based on ratio_NS>ratio_EW nested if statement)
    light_advance_NS= math.ceil(ratio_NS)
    light_advance_EW = math.ceil(ratio_EW)
    if ratio_NS > ratio_EW:
        time_selector=light_advance_NS
    else:
        time_selector=light_advance_EW

    #if statement to check what congestion response is needed
    if (time_selector-1)==0:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light) EDIT: ratio comparison incorrect, use prev light state instead.
                if prev_light_NS == "green":
                    #switching to other light
                    traffic_light_EW="green"
                    lightstate=0
                    traffic_light_NS="red"
                    prev_light_NS="red"
                    #set previous variables to current, resetting conditionals for next switching case
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    prev_light_advance_NS = light_advance_NS
                    prev_light_advance_EW = light_advance_EW

                    max_time=False
                    
                    #send state of light for NS: red=0
                    #send camera 
                    #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                    max_camera_count_E=0
                    max_camera_count_W=0
                    print("time 0 max NS OFF (EW ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    #switching to other light
                    traffic_light_NS="green"
                    lightstate=1
                    traffic_light_EW="red"
                    prev_light_EW="red"
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    prev_light_advance_NS = light_advance_NS
                    prev_light_advance_EW = light_advance_EW
                    #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                    max_camera_count_N=0
                    max_camera_count_S=0
                    max_time=False
                    print("time 0 max EW OFF (NS ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass

                # if traffic_light_NS == "red":
                #     #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                # else:
                #     #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":

                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_NS < prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_NS - prev_light_advance_NS == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_NS - prev_light_advance_NS == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_NS - prev_light_advance_NS == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_NS - prev_light_advance_NS == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_NS - prev_light_advance_NS == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_EW > prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_EW-light_advance_NS==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_EW-light_advance_NS==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_EW-light_advance_NS==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_EW-light_advance_NS==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_EW-light_advance_NS==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass

                elif traffic_light_EW == "green":
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_EW < prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_EW - prev_light_advance_EW == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_EW - prev_light_advance_EW == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_EW - prev_light_advance_EW == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_EW - prev_light_advance_EW == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_EW - prev_light_advance_EW == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_NS > prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_NS-light_advance_EW==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_NS-light_advance_EW==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_NS-light_advance_EW==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_NS-light_advance_EW==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_NS-light_advance_EW==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass
                prev_light_advance_NS=light_advance_NS
                prev_light_advance_EW=light_advance_EW
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_light_NS= "green"
                        prev_time_selector=(time_selector-1)
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
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
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS
                        #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_camera_count_S=0
                        max_camera_count_N=0
                        max_time=False
                        print("time 0 NS ON (EW OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_light_EW= "green"
                        prev_time_selector=(time_selector-1)
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS
                        #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
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
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS
                        #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                        max_camera_count_E=0
                        max_camera_count_W=0
                        max_time=False
                        print("time 0 EW ON (NS OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                # if traffic_light_NS == "red":
                #     #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                # else:
                #     #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":

                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_NS < prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_NS - prev_light_advance_NS == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_NS - prev_light_advance_NS == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_NS - prev_light_advance_NS == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_NS - prev_light_advance_NS == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_NS - prev_light_advance_NS == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_EW > prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_EW-light_advance_NS==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_EW-light_advance_NS==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_EW-light_advance_NS==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_EW-light_advance_NS==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_EW-light_advance_NS==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass

                elif traffic_light_EW == "green":
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_EW < prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_EW - prev_light_advance_EW == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_EW - prev_light_advance_EW == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_EW - prev_light_advance_EW == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_EW - prev_light_advance_EW == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_EW - prev_light_advance_EW == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_NS > prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_NS-light_advance_EW==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_NS-light_advance_EW==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_NS-light_advance_EW==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_NS-light_advance_EW==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_NS-light_advance_EW==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass
                prev_light_advance_NS=light_advance_NS
                prev_light_advance_EW=light_advance_EW
    elif (time_selector-1)==1:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if prev_light_NS == "green":
                    #switching to other light
                    traffic_light_EW="green"
                    lightstate=0
                    traffic_light_NS="red"
                    prev_light_NS="red"
                    #set previous variables to current, resetting conditionals for next switching case
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    prev_light_advance_NS = light_advance_NS
                    prev_light_advance_EW = light_advance_EW
                    max_time=False
                    #send state of light for NS: red=0
                    #send camera 
                    #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                    max_camera_count_E=0
                    max_camera_count_W=0
                    print("time 1 max NS OFF (EW ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    #switching to other light
                    traffic_light_NS="green"
                    lightstate=1
                    traffic_light_EW="red"
                    prev_light_EW="red"
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    prev_light_advance_NS = light_advance_NS
                    prev_light_advance_EW = light_advance_EW
                    #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                    max_camera_count_N=0
                    max_camera_count_S=0
                    max_time=False
                    print("time 1 max EW OFF (NS ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                # if traffic_light_NS == "red":
                #     #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                # else:
                #     #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":

                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_NS < prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_NS - prev_light_advance_NS == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_NS - prev_light_advance_NS == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_NS - prev_light_advance_NS == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_NS - prev_light_advance_NS == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_NS - prev_light_advance_NS == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_EW > prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_EW-light_advance_NS==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_EW-light_advance_NS==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_EW-light_advance_NS==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_EW-light_advance_NS==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_EW-light_advance_NS==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass

                elif traffic_light_EW == "green":
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_EW < prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_EW - prev_light_advance_EW == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_EW - prev_light_advance_EW == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_EW - prev_light_advance_EW == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_EW - prev_light_advance_EW == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_EW - prev_light_advance_EW == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_NS > prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_NS-light_advance_EW==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_NS-light_advance_EW==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_NS-light_advance_EW==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_NS-light_advance_EW==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_NS-light_advance_EW==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass
                prev_light_advance_NS=light_advance_NS
                prev_light_advance_EW=light_advance_EW
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_light_NS= "green"
                        prev_time_selector=(time_selector-1)
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
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
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_camera_count_S=0
                        max_camera_count_N=0
                        max_time=False
                        print("time 1 NS ON (EW OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_light_EW= "green"
                        prev_time_selector=(time_selector-1)
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
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
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS
                        #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                        max_camera_count_E=0
                        max_camera_count_W=0                        
                        max_time=False
                        print("time 1 EW ON (NS OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                # if traffic_light_NS == "red":
                #     #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                # else:
                #     #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":

                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_NS < prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_NS - prev_light_advance_NS == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_NS - prev_light_advance_NS == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_NS - prev_light_advance_NS == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_NS - prev_light_advance_NS == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_NS - prev_light_advance_NS == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_EW > prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_EW-light_advance_NS==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_EW-light_advance_NS==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_EW-light_advance_NS==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_EW-light_advance_NS==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_EW-light_advance_NS==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass

                elif traffic_light_EW == "green":
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_EW < prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_EW - prev_light_advance_EW == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_EW - prev_light_advance_EW == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_EW - prev_light_advance_EW == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_EW - prev_light_advance_EW == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_EW - prev_light_advance_EW == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_NS > prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_NS-light_advance_EW==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_NS-light_advance_EW==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_NS-light_advance_EW==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_NS-light_advance_EW==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_NS-light_advance_EW==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass
                prev_light_advance_NS=light_advance_NS
                prev_light_advance_EW=light_advance_EW
    elif (time_selector-1)==2:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if prev_light_NS == "green":
                    #switching to other light
                    traffic_light_EW="green"
                    lightstate=0
                    traffic_light_NS="red"
                    prev_light_NS="red"
                    #set previous variables to current, resetting conditionals for next switching case
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    prev_light_advance_NS = light_advance_NS
                    prev_light_advance_EW = light_advance_EW
                    max_time=False
                    
                    #send state of light for NS: red=0
                    #send camera 
                    #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                    max_camera_count_E=0
                    max_camera_count_W=0
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
                    prev_light_EW="red"
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    prev_light_advance_NS = light_advance_NS
                    prev_light_advance_EW = light_advance_EW
                    #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                    max_camera_count_N=0
                    max_camera_count_S=0
                    max_time=False
                    print("time 2 max EW OFF (NS ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                # if traffic_light_NS == "red":
                #     #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                # else:
                #     #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":

                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_NS < prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_NS - prev_light_advance_NS == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_NS - prev_light_advance_NS == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_NS - prev_light_advance_NS == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_NS - prev_light_advance_NS == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_NS - prev_light_advance_NS == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_EW > prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_EW-light_advance_NS==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_EW-light_advance_NS==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_EW-light_advance_NS==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_EW-light_advance_NS==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_EW-light_advance_NS==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass

                elif traffic_light_EW == "green":
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_EW < prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_EW - prev_light_advance_EW == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_EW - prev_light_advance_EW == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_EW - prev_light_advance_EW == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_EW - prev_light_advance_EW == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_EW - prev_light_advance_EW == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_NS > prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_NS-light_advance_EW==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_NS-light_advance_EW==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_NS-light_advance_EW==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_NS-light_advance_EW==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_NS-light_advance_EW==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass
                prev_light_advance_NS=light_advance_NS
                prev_light_advance_EW=light_advance_EW
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_light_NS= "green"
                        prev_time_selector=(time_selector-1)
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
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
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_camera_count_S=0
                        max_camera_count_N=0
                        max_time=False
                        print("time 2 NS ON (EW OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_light_EW= "green"
                        prev_time_selector=(time_selector-1)
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
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
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS
                        #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                        max_camera_count_E=0
                        max_camera_count_W=0                        
                        max_time=False
                        print("time 2 EW ON (NS OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                # if traffic_light_NS == "red":
                #     #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                # else:
                #     #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":

                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_NS < prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_NS - prev_light_advance_NS == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_NS - prev_light_advance_NS == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_NS - prev_light_advance_NS == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_NS - prev_light_advance_NS == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_NS - prev_light_advance_NS == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_EW > prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_EW-light_advance_NS==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_EW-light_advance_NS==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_EW-light_advance_NS==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_EW-light_advance_NS==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_EW-light_advance_NS==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass

                elif traffic_light_EW == "green":
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_EW < prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_EW - prev_light_advance_EW == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_EW - prev_light_advance_EW == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_EW - prev_light_advance_EW == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_EW - prev_light_advance_EW == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_EW - prev_light_advance_EW == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_NS > prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_NS-light_advance_EW==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_NS-light_advance_EW==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_NS-light_advance_EW==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_NS-light_advance_EW==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_NS-light_advance_EW==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass
                prev_light_advance_NS=light_advance_NS
                prev_light_advance_EW=light_advance_EW
    elif (time_selector-1)==3:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if prev_light_NS == "green":
                    #switching to other light
                    traffic_light_EW="green"
                    lightstate=0
                    traffic_light_NS="red"
                    prev_light_NS="red"                    
                    #set previous variables to current, resetting conditionals for next switching case
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    prev_light_advance_NS = light_advance_NS
                    prev_light_advance_EW = light_advance_EW
                    max_time=False
                    
                    #send state of light for NS: red=0
                    #send camera 
                    #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                    max_camera_count_E=0
                    max_camera_count_W=0
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
                    prev_light_EW="red"
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    prev_light_advance_NS = light_advance_NS
                    prev_light_advance_EW = light_advance_EW
                    #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                    max_camera_count_N=0
                    max_camera_count_S=0
                    max_time=False
                    print("time 3 max EW OFF (NS ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                # if traffic_light_NS == "red":
                #     #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                # else:
                #     #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":

                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_NS < prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_NS - prev_light_advance_NS == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_NS - prev_light_advance_NS == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_NS - prev_light_advance_NS == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_NS - prev_light_advance_NS == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_NS - prev_light_advance_NS == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_EW > prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_EW-light_advance_NS==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_EW-light_advance_NS==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_EW-light_advance_NS==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_EW-light_advance_NS==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_EW-light_advance_NS==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass

                elif traffic_light_EW == "green":
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_EW < prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_EW - prev_light_advance_EW == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_EW - prev_light_advance_EW == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_EW - prev_light_advance_EW == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_EW - prev_light_advance_EW == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_EW - prev_light_advance_EW == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_NS > prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_NS-light_advance_EW==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_NS-light_advance_EW==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_NS-light_advance_EW==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_NS-light_advance_EW==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_NS-light_advance_EW==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass
                prev_light_advance_NS=light_advance_NS
                prev_light_advance_EW=light_advance_EW
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_light_NS= "green"
                        prev_time_selector=(time_selector-1)
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
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
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_camera_count_S=0
                        max_camera_count_N=0
                        max_time=False
                        print("time 3 NS ON (EW OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_light_EW= "green"
                        prev_time_selector=(time_selector-1)
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
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
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS
                        #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                        max_camera_count_E=0
                        max_camera_count_W=0                        
                        max_time=False
                        print("time 3 EW ON (NS OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                # if traffic_light_NS == "red":
                #     #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                # else:
                #     #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":

                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_NS < prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_NS - prev_light_advance_NS == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_NS - prev_light_advance_NS == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_NS - prev_light_advance_NS == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_NS - prev_light_advance_NS == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_NS - prev_light_advance_NS == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_EW > prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_EW-light_advance_NS==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_EW-light_advance_NS==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_EW-light_advance_NS==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_EW-light_advance_NS==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_EW-light_advance_NS==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass

                elif traffic_light_EW == "green":
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_EW < prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_EW - prev_light_advance_EW == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_EW - prev_light_advance_EW == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_EW - prev_light_advance_EW == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_EW - prev_light_advance_EW == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_EW - prev_light_advance_EW == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_NS > prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_NS-light_advance_EW==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_NS-light_advance_EW==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_NS-light_advance_EW==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_NS-light_advance_EW==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_NS-light_advance_EW==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass
                prev_light_advance_NS=light_advance_NS
                prev_light_advance_EW=light_advance_EW
    elif (time_selector-1)==4:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if prev_light_NS == "green":
                    #switching to other light
                    traffic_light_EW="green"
                    lightstate=0
                    traffic_light_NS="red"
                    prev_light_NS="red"
                    #set previous variables to current, resetting conditionals for next switching case
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    prev_light_advance_NS = light_advance_NS
                    prev_light_advance_EW = light_advance_EW
                    max_time=False
                    
                    #send state of light for NS: red=0
                    #send camera 
                    #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                    max_camera_count_E=0
                    max_camera_count_W=0
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
                    prev_light_EW="red"
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    prev_light_advance_NS = light_advance_NS
                    prev_light_advance_EW = light_advance_EW
                    #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                    max_camera_count_N=0
                    max_camera_count_S=0
                    max_time=False
                    print("time 4 max EW OFF (NS ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                # if traffic_light_NS == "red":
                #     #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                # else:
                #     #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":

                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_NS < prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_NS - prev_light_advance_NS == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_NS - prev_light_advance_NS == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_NS - prev_light_advance_NS == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_NS - prev_light_advance_NS == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_NS - prev_light_advance_NS == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_EW > prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_EW-light_advance_NS==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_EW-light_advance_NS==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_EW-light_advance_NS==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_EW-light_advance_NS==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_EW-light_advance_NS==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass

                elif traffic_light_EW == "green":
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_EW < prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_EW - prev_light_advance_EW == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_EW - prev_light_advance_EW == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_EW - prev_light_advance_EW == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_EW - prev_light_advance_EW == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_EW - prev_light_advance_EW == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_NS > prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_NS-light_advance_EW==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_NS-light_advance_EW==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_NS-light_advance_EW==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_NS-light_advance_EW==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_NS-light_advance_EW==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass
                prev_light_advance_NS=light_advance_NS
                prev_light_advance_EW=light_advance_EW
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_light_NS= "green"
                        prev_time_selector=(time_selector-1)
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
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
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_camera_count_S=0
                        max_camera_count_N=0
                        max_time=False
                        print("time 4 NS ON (EW OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_light_EW= "green"
                        prev_time_selector=(time_selector-1)
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
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
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS
                        #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                        max_camera_count_E=0
                        max_camera_count_W=0                        
                        max_time=False
                        print("time 4 EW ON (NS OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                # if traffic_light_NS == "red":
                #     #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                # else:
                #     #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":

                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_NS < prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_NS - prev_light_advance_NS == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_NS - prev_light_advance_NS == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_NS - prev_light_advance_NS == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_NS - prev_light_advance_NS == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_NS - prev_light_advance_NS == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_EW > prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_EW-light_advance_NS==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_EW-light_advance_NS==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_EW-light_advance_NS==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_EW-light_advance_NS==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_EW-light_advance_NS==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass

                elif traffic_light_EW == "green":
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_EW < prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_EW - prev_light_advance_EW == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_EW - prev_light_advance_EW == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_EW - prev_light_advance_EW == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_EW - prev_light_advance_EW == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_EW - prev_light_advance_EW == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_NS > prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_NS-light_advance_EW==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_NS-light_advance_EW==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_NS-light_advance_EW==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_NS-light_advance_EW==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_NS-light_advance_EW==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass
                prev_light_advance_NS=light_advance_NS
                prev_light_advance_EW=light_advance_EW
    elif (time_selector-1)==5:
        #if statement to see if lights were previously green and thus, extended
        if max_time==True:
            #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                #if statement for ratio comparison (switch other light)
                if prev_light_NS == "green":
                    #switching to other light
                    traffic_light_EW="green"
                    lightstate=0
                    traffic_light_NS="red"
                    prev_light_NS="red"
                    #set previous variables to current, resetting conditionals for next switching case
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    prev_light_advance_NS = light_advance_NS
                    prev_light_advance_EW = light_advance_EW
                    max_time=False
                    
                    #send state of light for NS: red=0
                    #send camera 
                    #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                    max_camera_count_E=0
                    max_camera_count_W=0
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
                    prev_light_EW="red"
                    prevlight_runtime=runtime
                    prev_time_selector=(time_selector-1)
                    prev_light_advance_NS = light_advance_NS
                    prev_light_advance_EW = light_advance_EW
                    #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                    max_camera_count_N=0
                    max_camera_count_S=0
                    max_time=False
                    print("time 5 max EW OFF (NS ON)")
                    print("ratio_NS: {}".format(ratio_NS))
                    print("ratio_EW: {}".format(ratio_EW))
                    print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                # if traffic_light_NS == "red":
                #     #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                # else:
                #     #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":

                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_NS < prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_NS - prev_light_advance_NS == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_NS - prev_light_advance_NS == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_NS - prev_light_advance_NS == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_NS - prev_light_advance_NS == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_NS - prev_light_advance_NS == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_EW > prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_EW-light_advance_NS==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_EW-light_advance_NS==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_EW-light_advance_NS==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_EW-light_advance_NS==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_EW-light_advance_NS==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass

                elif traffic_light_EW == "green":
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_EW < prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_EW - prev_light_advance_EW == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_EW - prev_light_advance_EW == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_EW - prev_light_advance_EW == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_EW - prev_light_advance_EW == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_EW - prev_light_advance_EW == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_NS > prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_NS-light_advance_EW==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_NS-light_advance_EW==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_NS-light_advance_EW==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_NS-light_advance_EW==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_NS-light_advance_EW==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass
                prev_light_advance_NS=light_advance_NS
                prev_light_advance_EW=light_advance_EW
        else:
            #another if statement to see if previous lights have done their time
            if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                #if statement for ratio comparison 
                if ratio_NS>ratio_EW:
                    #switch ratio_NS, if statement for red light or green
                    if traffic_light_NS == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_light_NS= "green"
                        prev_time_selector=(time_selector-1)
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
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
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                        max_camera_count_S=0
                        max_camera_count_N=0
                        max_time=False
                        print("time 5 NS ON (EW OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
                else:
                    if traffic_light_EW == "green":
                        prevlight_runtime=runtime
                        #extend lights on green
                        prev_light_EW= "green"
                        prev_time_selector=(time_selector-1)
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS

                        #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
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
                        prev_light_advance_EW = light_advance_EW
                        prev_light_advance_NS = light_advance_NS
                        #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                        max_camera_count_E=0
                        max_camera_count_W=0                        
                        max_time=False
                        print("time 5 EW ON (NS OFF)")
                        print("ratio_NS: {}".format(ratio_NS))
                        print("ratio_EW: {}".format(ratio_EW))
                        print("length of light: {}".format(light_time_length[prev_time_selector]))
            else:
                #send # of car 
                #pass
                # if traffic_light_NS == "red":
                #     #ser.write(pack('5h',max_camera_count_S,max_camera_count_N,camera_count_E,camera_count_W,lightstate))
                # else:
                #     #ser.write(pack('5h',camera_count_S,camera_count_N,max_camera_count_E,max_camera_count_W,lightstate))
                #if statement to ensure that a green-lit direction's ratio will be compared with the ratio that set the green light.
                if traffic_light_NS == "green":

                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_NS < prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_NS - prev_light_advance_NS == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_NS - prev_light_advance_NS == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_NS - prev_light_advance_NS == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_NS - prev_light_advance_NS == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_NS - prev_light_advance_NS == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_EW > prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_EW-light_advance_NS==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_EW-light_advance_NS==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_EW-light_advance_NS==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_EW-light_advance_NS==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_EW-light_advance_NS==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass

                elif traffic_light_EW == "green":
                    #conditionals to check level of traffic. if ==0 means its still heavy traffic, elif ==1 then current traffic is lower by 1 level, runtime increases by an additional +1 to speed up the green light
                    if (light_advance_EW < prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        runtime+=1
                        if light_advance_EW - prev_light_advance_EW == -5:
                            runtime+=3
                            print("if statement 1:-5")
                        elif light_advance_EW - prev_light_advance_EW == -4:
                            runtime+=2
                            print("if statement 1:-4")
                        elif light_advance_EW - prev_light_advance_EW == -3:
                            runtime+=2
                            print("if statement 1:-3")
                        elif light_advance_EW - prev_light_advance_EW == -2:
                            runtime+=1
                            print("if statement 1:-2")
                        elif light_advance_EW - prev_light_advance_EW == -1:
                            print("if statement 1:-1")
                            pass
                        else:
                            print("if statement 1:none")
                            pass
                    if (light_advance_NS > prev_light_advance_NS) & (runtime-prevlight_runtime>5):
                        print("light_advanceNS:", light_advance_NS)
                        print("prev_light_advanceNS:", prev_light_advance_NS)
                        runtime+=1
                        print("if statement 2 redlight>prev_redlight")
                    
                    if (light_advance_NS == prev_light_advance_NS) & (light_advance_EW == prev_light_advance_EW) & (runtime-prevlight_runtime>5):
                        if light_advance_NS-light_advance_EW==5:
                            runtime+=4
                            print("if statement 3:5")
                        elif light_advance_NS-light_advance_EW==4:
                            runtime+=3
                            print("if statement 3:4")
                        elif light_advance_NS-light_advance_EW==3:
                            runtime+=2
                            print("if statement 3:3")
                        elif light_advance_NS-light_advance_EW==2:
                            runtime+=1
                            print("if statement 3:2")
                        elif light_advance_NS-light_advance_EW==1:
                            runtime+=1
                            print("if statement 3:1")
                        else:
                            print("if statement 3:none")
                            pass
                    
                    pass
                prev_light_advance_NS=light_advance_NS
                prev_light_advance_EW=light_advance_EW


    if array_counter<10:
        array_counter+=1
    else:
        array_counter=10
