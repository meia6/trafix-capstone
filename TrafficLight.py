# Each intersection contains two traffic lights, but for now only one "traffic"

from time import cmtime

class TrafficLight:
    def __init__(self, start_color):
        self.status = start_color
        self.hold_time = 0
        cars = 0
    
    def change_color(self):  # yellow lights will be considered at a later stage
        if(self.status == "green"):
            self.set_red
        elif(self.status == "red"):
            self.set_green
        self.send_status()

    def set_green(self):
        self.status = "green"
        self.hold_time = 0
    
    def set_yellow(self):
        self.status = "yellow"
        self.hold_time = 0
    
    def set_red(self):
        self.status = "red"
        self.hold_time = 0

    def set_car_count(self, count):
        self.cars = count
    
    def get_hold_time(self):
        return self
    
    def get_cars(self):
        return self.cars

    def send_status(self):  # send current status to microcontroller to display lights
        return self.status