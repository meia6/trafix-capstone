import time
import TrafficLight

class Intersection:  # modify to store data like in proposed SQL db
    def __init__(self, name, traffic_lights):
        # intersection name
        # street 1 ~ 4 (street class)
        # camera 1 ~ 4 (corresponds to each street)
        self.traffic_lights = traffic_lights
        self.name = name  # street name, e.g. MainW_Cootes

    def compare_congestion(self):
        ns_congestion = self.lightNS.get_congestion()
        ew_congestion = self.lightEW.get_congestion()
        return ns_congestion / ew_congestion

    # def process_light(self):
        
    def get_green_direction(self):
        if(self.lightNS.get_status() == "green"):
            return "NS"
        if(self.lightEW.get_status() == "green"):
            return "EW"
        return "Transitioning"  # if neither light is green (one light is yellow/both are red)

    def change_color(self, target_hold_time):
        if(self.lightNS.status == "green"):
            self.lightNS.set_red()
            self.lightEW.set_green(target_hold_time)

        elif(self.lightNS.status == "red"):
            self.lightEW.set_red()
            self.lightNS.set_green(target_hold_time)

    def get_lightNS(self):
        return self.lightNS
    
    def get_lightEW(self):
        return self.lightEW
    
    def get_traffic_lights(self):
        return self.traffic_lights
    