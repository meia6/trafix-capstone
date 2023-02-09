# Each intersection contains two traffic lights, but for now only one "traffic"

import time

class TrafficLight:
    def __init__(self, start_color, congestion_counts, congestion_timings):
        self.status = start_color
        self.hold_time = 0
        self.crosswalk_request = False  # true when a crosswalk request is pending (button is pressed)
        self.crosswalk_status = False  # true when pedestrian may cross
        self.congestion_counts = congestion_counts
        self.congestion_timings = congestion_timings

        if (len(congestion_counts) != len(congestion_timings)):
            print("Warning: congestion levels and timings array length differ")

    def set_green(self, target_duration):
        self.status = "green"
        self.hold_time = 0
        self.target_duration = target_duration
        self.green_start_time = time.gmtime()

        if (self.crosswalk_request):
            self.crosswalk_status = True
            self.crosswalk_request = False
    
    def set_yellow(self):
        self.status = "yellow"
        self.hold_time = 0
    
    def set_red(self):
        self.status = "red"
        self.hold_time = 0
    
    def get_hold_time(self):
        return self.hold_time
    
    def get_status(self):
        return self.status
    
    def send_status(self):  # send current status to microcontroller to display lights
        return self.status
    
    def crosswalk_pressed(self):
        self.crosswalk_request = True

    def get_congestion(self):
        for i in reversed(range(len(self.congestion_counts))):  # ~3 or 4 congestion levels max
            if (self.count_cars >= self.congestion_counts[i]):
                return i + 1

    def count_cars(self):  # intake arduino output thing and return it
        return 0
    
    def check_time(self):
        if()