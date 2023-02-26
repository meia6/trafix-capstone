import Street

class TrafficLight:
    def __init__(self, name, street, redlight_min, crosswalk_min, greenlight_max, camera):
        self.name = name
        self.street = street
        self.min_time = redlight_min
        self.max_time = greenlight_max
        self.min_crosswalk = crosswalk_min
        self.crosswalk_status = False
        self.crosswalk_request = False
        self.status = False  # false = red, green = true
        self.camera = camera
		
    def set_cross_status(self, status):
        self.crosswalk_status = status
		
    def set_cross_request(self, request):
        self.crosswalk_request = request
		
    def set_mintime(self, min):
        self.min_time = min
	
    def set_maxtime(self, max):
        self.max_time = max
		
    def set_mincrosswalk(self, min_cross):
        self.min_crosswalk = min_cross
		
    def set_status(self, newStatus):
        self.status = newStatus
		
    def set_street(self, newStreet):
        self.set_street = newStreet
		
    def change_name(self, newName):
        self.name = newName
	
    def get_status(self):
        return self.status
    
    def send_status(self):  # send current color to microcontroller to display lights
        return self.status
    
    def crosswalk_pressed(self):
        self.crosswalk_request = True

    def set_camera(self, camera):
        self.camera = camera
    
    def get_camera(self, camera):
        return self.camera