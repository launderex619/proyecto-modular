class drone_data_receiver_module:
    def __init__(self):
        self.input_video = None
        self.video_duration_secs = None
        self.drone_camera_props = None
        self.flight_units = None              # [D, H, DS, VS] by second
        self.drone_ = None



    def get_video_path(self):
        pass

    def get_video_duration(self):
        pass
        
    def get_frames(self, second):
        pass

    def get_fligth_units(self, second):
        pass

    def get_gps_location(self, second):
        pass

    def get_drone_quaternion(self, second):
        pass

    def get_drone_velocity(self, second):
        pass

    def get_drone_acceleration(self, second):
        pass

    def get_drone_attitude(self, second):
        pass

    def get_drone_angular_velocity(self, second):
        pass

    def get_drone_angular_acceleration(self, second):
        pass

    def get_drone_camera_props(self, second):
        pass

    def get_drone_camera_image(self, second):
        pass
