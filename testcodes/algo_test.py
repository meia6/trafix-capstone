import time
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import urllib.request
import numpy as np
from cvlib.object_detection import draw_bbox
import concurrent.futures
import VideoInput
# Main driver file


program_running = True

intersections = []
selector=0
runtime=0
prevlight_runtime=0
video_frame_count=0
while(program_running):
    
    video_frame_count,camera_count_N=VideoInput.video_input('traffic1.mp4',video_frame_count)
    print(video_frame_count)
    print(camera_count_N)
    
    for intersection in intersections:  # there will be 2 - 3 intersections max
        camera_counts = [camera_count_N,camera_count_E,camera_count_S,camera_count_W]
        traffic_lights = intersection.traffic_lights
        #for i in range(len(intersection.traffic_lights)):  # scan file to get traffic count for all 4 cameras. Index 0 and 2, 1 and 3 are opposite of each other
        #    traffic_data = open("%s.txt" % intersection.traffic_lights[i].get_camera, "r")  # contains the number of cars detected in each camera
        #    camera_counts[i] = traffic_data.read() 
        #    #timing is polling-based. This is done according to how often we sample the camera car counts.

        #threshold is the # of cars in the direction that will be a problem to us (# of cars that is considered as traffic)
        #speed_limit
        threshold_NS=5
        threshold_EW=2
        ratio_NS = (camera_counts[0] + camera_counts[2]) /  threshold_NS #ex. if ratio=1, base traffic congestion. call light_time_length[1].
        ratio_EW = (camera_counts[1] + camera_counts[3]) / threshold_EW #if ratio=2, 2nd level of traffic congestion. call light_time_length[2].
        light_time_length=[60,120,180,240,300]#1,2,3,4,5 mins
        min_time_light= [10,20,30,40,50,60]
        max_time_light= [10,20,30,40,50,60]
        #if statement to decide congestion level (might be redundant based on ratio_NS>ratio_EW nested if statement)
        if ratio_NS > ratio_EW:
            time_selector=ratio_NS
        else:
            time_selector=ratio_EW

        #if statement to check what congestion response is needed
        if time_selector==0:
            #if statement to see if lights were previously green and thus, extended
            if max_time==True:
                #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                    #if statement for ratio comparison (switch other light)
                    if ratio_NS>ratio_EW==True:
                        #switching to other light
                        prevlight_runtime=runtime
                        prev_time_selector=ratio_EW
                        light_time_length[ratio_EW] #call this extra?
                        max_time=False
                        #send state of light for NS: red=0
                        #send camera 
                    else:
                        #switching to other light
                        prevlight_runtime=runtime
                        prev_time_selector=ratio_NS
                        light_time_length[ratio_NS] #call this extra?
                        max_time=False
                else:
                    #send # of car 
                    pass
            else:
                #another if statement to see if previous lights have done their time
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                    #if statement for ratio comparison 
                    if ratio_NS>ratio_EW==True:
                        #switch ratio_NS, if statement for red light or green
                        if traffic_light == "green":
                            prevlight_runtime=runtime
                            #extend lights on green
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS] #call this extra?
                            max_time=True
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS]
                            max_time=False
                    else:
                        if traffic_light == "green":
                            prevlight_runtime=runtime
                            #extend lights on green
                            prev_time_selector=ratio_EW
                            light_time_length[ratio_EW] #call this extra?
                            max_time=True
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_EW
                            light_time_length[ratio_EW]
                            max_time=False
                else:
                    pass
        elif time_selector==1:
            #if statement to see if lights were previously green and thus, extended
            if max_time==True:
                #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                    #if statement for ratio comparison (switch other light)
                    if ratio_NS>ratio_EW==True:
                        #switching to other light
                        prevlight_runtime=runtime
                        prev_time_selector=ratio_EW
                        light_time_length[ratio_EW] #call this extra?
                        max_time=False
                        
                    else:
                        #switching to other light
                        prevlight_runtime=runtime
                        prev_time_selector=ratio_NS
                        light_time_length[ratio_NS] #call this extra?
                        max_time=False
                else:
                    pass
            else:
                #another if statement to see if previous lights have done their time
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                    #if statement for ratio comparison 
                    if ratio_NS>ratio_EW==True:
                        #switch ratio_NS, if statement for red light or green
                        if traffic_light == "green":
                            prevlight_runtime=runtime
                            #extend lights on green
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS] #call this extra?
                            max_time=True
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS]
                            max_time=False
                    else:
                        if traffic_light == "green":
                            prevlight_runtime=runtime
                            #extend lights on green
                            prev_time_selector=ratio_EW
                            light_time_length[ratio_EW] #call this extra?
                            max_time=True
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_EW
                            light_time_length[ratio_EW]
                            max_time=False
                else:
                    pass
        elif time_selector==2:
            #if statement to see if lights were previously green and thus, extended
            if max_time==True:
                #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                    #if statement for ratio comparison (switch other light)
                    if ratio_NS>ratio_EW==True:
                        #switching to other light
                        prevlight_runtime=runtime
                        prev_time_selector=ratio_EW
                        light_time_length[ratio_EW] #call this extra?
                        max_time=False
                        
                    else:
                        #switching to other light
                        prevlight_runtime=runtime
                        prev_time_selector=ratio_NS
                        light_time_length[ratio_NS] #call this extra?
                        max_time=False
                else:
                    pass
            else:
                #another if statement to see if previous lights have done their time
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                    #if statement for ratio comparison 
                    if ratio_NS>ratio_EW==True:
                        #switch ratio_NS, if statement for red light or green
                        if traffic_light == "green":
                            prevlight_runtime=runtime
                            #extend lights on green
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS] #call this extra?
                            max_time=True
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS]
                            max_time=False
                    else:
                        if traffic_light == "green":
                            prevlight_runtime=runtime
                            #extend lights on green
                            prev_time_selector=ratio_EW
                            light_time_length[ratio_EW] #call this extra?
                            max_time=True
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_EW
                            light_time_length[ratio_EW]
                            max_time=False
                else:
                    pass
        elif time_selector==3:
            #if statement to see if lights were previously green and thus, extended
            if max_time==True:
                #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                    #if statement for ratio comparison (switch other light)
                    if ratio_NS>ratio_EW==True:
                        #switching to other light
                        prevlight_runtime=runtime
                        prev_time_selector=ratio_EW
                        light_time_length[ratio_EW] #call this extra?
                        max_time=False
                        
                    else:
                        #switching to other light
                        prevlight_runtime=runtime
                        prev_time_selector=ratio_NS
                        light_time_length[ratio_NS] #call this extra?
                        max_time=False
                else:
                    pass
            else:
                #another if statement to see if previous lights have done their time
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                    #if statement for ratio comparison 
                    if ratio_NS>ratio_EW==True:
                        #switch ratio_NS, if statement for red light or green
                        if traffic_light == "green":
                            prevlight_runtime=runtime
                            #extend lights on green
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS] #call this extra?
                            max_time=True
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS]
                            max_time=False
                    else:
                        if traffic_light == "green":
                            prevlight_runtime=runtime
                            #extend lights on green
                            prev_time_selector=ratio_EW
                            light_time_length[ratio_EW] #call this extra?
                            max_time=True
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_EW
                            light_time_length[ratio_EW]
                            max_time=False
                else:
                    pass
        elif time_selector==4:
            #if statement to see if lights were previously green and thus, extended
            if max_time==True:
                #another if statement to see if previous lights have done their time (in this block, make the switch to the other lights regardless)
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]+max_time_light[prev_time_selector]:
                    #if statement for ratio comparison (switch other light)
                    if ratio_NS>ratio_EW==True:
                        #switching to other light
                        prevlight_runtime=runtime
                        prev_time_selector=ratio_EW
                        light_time_length[ratio_EW] #call this extra?
                        max_time=False
                        
                    else:
                        #switching to other light
                        prevlight_runtime=runtime
                        prev_time_selector=ratio_NS
                        light_time_length[ratio_NS] #call this extra?
                        max_time=False
                else:
                    pass
            else:
                #another if statement to see if previous lights have done their time
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                    #if statement for ratio comparison 
                    if ratio_NS>ratio_EW==True:
                        #switch ratio_NS, if statement for red light or green
                        if traffic_light == "green":
                            prevlight_runtime=runtime
                            #extend lights on green
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS] #call this extra?
                            max_time=True
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS]
                            max_time=False
                    else:
                        if traffic_light == "green":
                            prevlight_runtime=runtime
                            #extend lights on green
                            prev_time_selector=ratio_EW
                            light_time_length[ratio_EW] #call this extra?
                            max_time=True
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_EW
                            light_time_length[ratio_EW]
                            max_time=False
                else:
                    pass
