class DroneTrackEntity:
    def __init__(self):
        self.input_video = None
        self.video_duration_secs = None
        self.drone_entity = None
        self.start_time = None

    def set_video_duration_secs(self, video_duration_secs):
        self.video_duration_secs = video_duration_secs
