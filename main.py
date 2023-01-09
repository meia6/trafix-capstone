from traffic import traffic_init
from camera import camera_init

# Main driver file

# Algorithm baseline
# 1. Receive traffic camera data from camera
# 2. Determine location + direction of camera
# 3. Get number of cars detected and store in 2d array (for now, later on we can try using a graph)
# 4. Repeat for all cameras
# 5. For each camera, take the respective neighboring traffic lights going in the same direction  
# 6. compare cars with camera corresponding to same direction
# 7. 

def __main__():

    # will standardize units later
    # speed_limit = 60  # km / h
    # distances = [0.4, 0.4]  # distance in km between intersections
    # max_hold_time = 120  # seconds
    # min_hold_time = 5  # seconds
    camera_init()
    traffic_init()
    # traffic_init(speed_limit, distances, max_hold_time, min_hold_time)
    