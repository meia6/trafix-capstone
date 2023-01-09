import Intersection
import TrafficLight

from time import gmtime

def traffic_init(speed_limit, distances, max_hold_time, min_hold_time):

    start_time = gmtime()

    intersections = [
        Intersection(TrafficLight("green"), TrafficLight("red"), start_time),
        Intersection(TrafficLight("red"), TrafficLight("green"), start_time)
    ]

    # To-do: multi-threading, timings using time import
    while(True):
        for intersection in intersections:

            if(intersection.get_hold_time() > max_hold_time):  # if max light hold time is reached, swap unconditionally
                intersection.change_color()
            # elif(intersection.compare_ns_ew() == True):  # check if NS direction has more cars than EW direction
            elif not (intersection.get_hold_time() < min_hold_time):
                intersection.light_transition()
