import time

class Intersection:
    def __init__(self, lightNS, lightEW):
        self.lightNS = lightNS
        self.lightEW = lightEW

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
            self.lightNS.set_yellow()
            time.sleep(2)
            self.lightNS.set_red()
            time.sleep(1)
            self.lightEW.set_green(target_hold_time)

        elif(self.lightNS.status == "red"):
            self.lightEW.set_yellow()
            time.sleep(2)
            self.lightEW.set_red()
            time.sleep(1)
            self.lightNS.set_green(target_hold_time)

    def get_lightNS(self):
        return self.lightNS
    
    def get_lightEW(self):
        return self.lightEW
    