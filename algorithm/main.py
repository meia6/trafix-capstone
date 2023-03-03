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
        #light_time_length=[60,120,180,240,300]/1,2,3,4,5 mins
        #min_time_light= [10,20,30,40,50,60]
        #if runtime-prevlight_time>light_time_length[], run code. If not, pass. (use try except blocks?)
            if ratio_NS>ratio_EW==True:
                #do light switch if its red.
                #switch ratio_NS, each case will send the corresponding time for the lights
            else:
                #do light switch if its red (if statement)
                #switch ratio_EW, each case will send the corresponding time for the lights
             

    