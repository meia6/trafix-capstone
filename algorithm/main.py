import Intersection
import TrafficLight

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


from time import gmtime

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

    ratio = (camera_counts[0] + camera_counts[2]) / (camera_counts[1] + camera_counts[3])
    