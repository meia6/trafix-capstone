
class Street:
    def __init__(self, name, speed_limit, distance, camera, num_of_cars):
        self.name = name
        self.speed_limit = speed_limit
        self.distance = distance
        self.camera = camera
        self.num_of_cars = num_of_cars

    def set_connection(self, street):
        self.connection = street

    def set_num_of_cars(self, num_of_cars):
        self.num_of_cars = num_of_cars
       