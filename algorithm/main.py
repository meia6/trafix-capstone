import Intersection
import TrafficLight
import time
# Main driver file

def __main__():

    # standardize units later
    # speed_limit = 60  # km / h
    # distances = [0.4, 0.4]      # distance in km between intersections
    # max_hold_time = 120         # seconds
    # min_hold_time = 5           # seconds
    # ped_min_hold_time = 20      # seconds
    traffic_init()
    # traffic_init(speed_limit, distances, max_hold_time, min_hold_time)



def traffic_init(speed_limit, distances, max_hold_time, min_hold_time, ped_min_hold_time):

    program_running = True

    intersections = []
    selector=0
    runtime=0
    prevlight_runtime=0
    while(program_running):
        for intersection in intersections:  # there will be 2 - 3 intersections max
            camera_counts = []
            traffic_lights = intersection.traffic_lights
            for i in range(len(intersection.traffic_lights)):  # scan file to get traffic count for all 4 cameras. Index 0 and 2, 1 and 3 are opposite of each other
                traffic_data = open("%s.txt" % intersection.traffic_lights[i].get_camera, "r")  # contains the number of cars detected in each camera
                camera_counts[i] = traffic_data.read() 
                #timing is polling-based. This is done according to how often we sample the camera car counts.

            #threshold is the # of cars in the direction that will be a problem to us (# of cars that is considered as traffic)
            #speed_limit
            threshold_NS=5
            threshold_EW=2
            ratio_NS = (camera_counts[0] + camera_counts[2]) /  threshold_NS #ex. if ratio=1, base traffic congestion. call light_time_length[1].
            ratio_EW = (camera_counts[1] + camera_counts[3]) / threshold_EW #if ratio=2, 2nd level of traffic congestion. call light_time_length[2].
            light_time_length=[60,120,180,240,300]#1,2,3,4,5 mins
            min_time_light= [10,20,30,40,50,60]

            #if statement to decide congestion level (might be redundant based on ratio_NS>ratio_EW nested if statement)
            if ratio_NS > ratio_EW:
                time_selector=ratio_NS
            else:
                time_selector=ratio_EW

        #if statement to check what congestion response is needed
            if time_selector==0:
                #another if statement to see if previous lights have done their time
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                    #if statement for ratio comparison 
                    if ratio_NS>ratio_EW==True:
                        #switch ratio_NS, if statement for red light or green
                        if traffic_light == "red":
                            prevlight_runtime=runtime
                            #extend lights on red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS] #call this extra?
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS]
                    else:
                        if traffic_light == "red":
                            prevlight_runtime=runtime
                            #extend lights on red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS] #call this extra?
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS]
                else:
                    pass
            elif time_selector==1:
                #another if statement to see if previous lights have done their time
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                    #if statement for ratio comparison 
                    if ratio_NS>ratio_EW==True:
                        #switch ratio_NS, if statement for red light or green
                        if traffic_light == "red":
                            prevlight_runtime=runtime
                            #extend lights on red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS] #call this extra?
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS]
                    else:
                        if traffic_light == "red":
                            prevlight_runtime=runtime
                            #extend lights on red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS] #call this extra?
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS]
                else:
                    pass
            elif time_selector==2:
                #another if statement to see if previous lights have done their time
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                    #if statement for ratio comparison 
                    if ratio_NS>ratio_EW==True:
                        #switch ratio_NS, if statement for red light or green
                        if traffic_light == "red":
                            prevlight_runtime=runtime
                            #extend lights on red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS] #call this extra?
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS]
                    else:
                        if traffic_light == "red":
                            prevlight_runtime=runtime
                            #extend lights on red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS] #call this extra?
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS]
                else:
                    pass
            elif time_selector==3:
                #another if statement to see if previous lights have done their time
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                    #if statement for ratio comparison 
                    if ratio_NS>ratio_EW==True:
                        #switch ratio_NS, if statement for red light or green
                        if traffic_light == "red":
                            prevlight_runtime=runtime
                            #extend lights on red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS] #call this extra?
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS]
                    else:
                        if traffic_light == "red":
                            prevlight_runtime=runtime
                            #extend lights on red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS] #call this extra?
                        else:
                            prevlight_runtime=runtime
                            #switch lights to red
                            prev_time_selector=ratio_NS
                            light_time_length[ratio_NS]
                else:
                    pass
            elif time_selector==4:
                #keep this code just in case above statements are brick, reset point
                if runtime-prevlight_runtime>light_time_length[prev_time_selector]:
                    if ratio_NS>ratio_EW==True:
                        prevlight_runtime=runtime
                        #do light switch if its red.
                        #switch ratio_NS, each case will send the corresponding time for the lights
                    else:
                        hi=0#do light switch if its red (if statement)
                        #switch ratio_EW, each case will send the corresponding time for the lights
                else:
                    pass


             

    