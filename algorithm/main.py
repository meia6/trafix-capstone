from traffic import traffic_init
from camera import camera_init

# Main driver file

def __main__():

    # standardize units later
    # speed_limit = 60  # km / h
    # distances = [0.4, 0.4]  # distance in km between intersections
    # max_hold_time = 120  # seconds
    # min_hold_time = 5  # seconds
    camera_init()
    traffic_init()
    # traffic_init(speed_limit, distances, max_hold_time, min_hold_time)
    