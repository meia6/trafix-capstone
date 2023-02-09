import Intersection
import TrafficLight

from time import gmtime

def traffic_init(speed_limit, distances, max_hold_time, min_hold_time, ped_min_hold_time):

    test_congestion_timings = [30, 50, 60]
    test_congestion_counts = [7, 20, 40]  # threshold for number of cars stalled for each congestion level

    intersections = [
        Intersection(TrafficLight("green", test_congestion_counts, test_congestion_timings),
                     TrafficLight("red", test_congestion_counts, test_congestion_timings)),
        Intersection(TrafficLight("red", test_congestion_counts, test_congestion_timings),
                     TrafficLight("green", test_congestion_counts, test_congestion_timings))
    ]

    while(True):
        for intersection in intersections:  # there will be 2 - 3 intersections max

            if(intersection.get_green_direction() == "NS"):  # if max light hold time is reached, swap unconditionally
                if(intersection.get)
            elif(intersection.get_green_direction() == "EW"):

                intersection.change_color(max(, ped_min_hold_time))
            elif not (intersection.get_hold_time() < min_hold_time):
                intersection.process_light()


    return 0