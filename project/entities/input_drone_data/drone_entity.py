class DroneEntity:
    def __init__(self):
        self.id = None                              # int  - Drone ID
        self.time = None                            # float - Time of the drone data
        self.attitude_roll = None                   # float - Attitude Roll of the drone
        self.attitude_pitch = None                  # float - Attitude Pitch of the drone
        self.attitude_yaw = None                    # float - Attitude Yaw of the drone
        self.altitude = None                        # float - Altitude of the drone
        self.speed = None                           # float - Speed of the drone
        self.velocity = None                        # float - Velocity of the drone
        self.acc = None                             # float - Acceleration of the drone
        self.gyr = None                             # float - Gyroscope of the drone
        self.mag = None                             # float - Magnetometer of the drone
        self.baro = None                            # float - Barometer of the drone
        self.baro_temp = None                       # float - Barometer temperature of the drone
        self.imu_temp = None                        # float - IMU temperature of the drone
        self.roll = None                            # float - Roll of the drone
        self.pitch = None                           # float - Pitch of the drone
        self.thor = None                            # float - Thrust of the drone   
        self.yaw = None                             # float - Yaw of the drone
        self.motors = None                          # float - Motors of the drone in array format [motor1, motor2, motor3, motor4]           
        self.latitude = None                        # float - Latitude of the drone 
        self.longitude = None                       # float - Longitude of the drone           
        self.angle = None                           # float - Angle of the drone 
        self.front_rear_tilt_angle = None           # float - Front/Rear tilt angle of the drone
        self.left_right_tilt_angle = None           # float - Left/Right tilt angle of the drone
        self.error = None                           # float - Error of the drone in distance in meters          
        self.d = None                               # float - Distance of the drone from the user drivining it           
        self.h = None                               # float - Height of the drone relative to the user driving it                    
        self.ds = None                              # float - Horizontal velocity of the drone
        self.vs = None                              # float - Vertical velocity of the drone

    def is_valid(self) -> bool:
        """
        This function checks if the entity is valid.
        :return: True if the entity is valid, False otherwise.
        """
        return self.time is not None
