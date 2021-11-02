class DroneTrackEntity:
    def __init__(self):
        self.input_video = None
        self.video_duration_secs = None
        self.drone_entity = []
        self.start_time = None
        self.end_time = None

    def set_video_duration_secs(self, video_duration_secs):
        self.video_duration_secs = video_duration_secs

    def add_drone_entity(self, drone_entity):
        self.drone_entity.append(drone_entity)

    def set_video_duration_secs(self, video_duration_secs):
        self.video_duration_secs = video_duration_secs

    def get_drone_entity_at_index(self, index):
        return self.drone_entity[index]

    def get_drone_entity_count(self):
        return len(self.drone_entity)

    def set_end_time(self, end_time):
        self.end_time = end_time

    def set_input_video(self, input_video):
        self.input_video = input_video
