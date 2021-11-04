class DroneTrackEntity:
    def __init__(self):
        self.input_video = None
        self.video_duration_secs = None
        self.drone_entities = []
        self.start_time = None
        self.end_time = None

    def set_video_duration_secs(self, video_duration_secs):
        self.video_duration_secs = video_duration_secs

    def add_drone_entity(self, drone_entity):
        self.drone_entities.append(drone_entity)

    def set_video_duration_secs(self, video_duration_secs):
        self.video_duration_secs = video_duration_secs

    def get_drone_entity_at_index(self, index):
        return self.drone_entities[index]

    def get_drone_entity_count(self):
        return len(self.drone_entities)

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_end_time(self, end_time):
        self.end_time = end_time

    def set_input_video(self, input_video):
        self.input_video = input_video
