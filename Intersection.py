from time import gmtime

class Intersection:
    def __init__(self, lightNS, lightEW, start_time):
        self.start_time = start_time
        self.lightNS = lightNS
        self.lightEW = lightEW

    def compare_ns_ew(self):
        if(self.lightNS.get_cars >= self.lightEW.get_cars):
            return True
        return False

    def light_transition(self):
        if(self.compare_ns_ew() & self.lightNS == "Green"):
            return
            
        if(self.lightNS.status == "Green"):
            self.lightNS.set_yellow()
            # wait for ~3 seconds, to be implemented
            self.lightNS.set_red()
            # wait for ~1 second, to be implemented
            self.lightEW.set_green()

        elif(self.lightNS.status == "Red"):
            self.lightEW.set_yellow()
            # wait for ~3 seconds, to be implemented
            self.lightEW.set_red()
            # wait for ~1 second, to be implemented
            self.lightNS.set_green()