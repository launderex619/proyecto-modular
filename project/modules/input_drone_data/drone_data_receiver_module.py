from controllers import ScrapperController


class DroneDataReceiverModule:
    """
    This class is responsible for receiving the drone data from the drone.
    """

    def __init__(self, drone_video_file_path, drone_data_file_path):
        """
        Initializes the drone data receiver module.
        :param drone_info_file_path: The path of the file containing the drone information.
        """
        self.drone_video_file_path = drone_video_file_path
        self.drone_data_file_path = drone_data_file_path
        self.drone_track_entity = None
        self.scrapper_controller = ScrapperController()
        self.start_scrapping()

    def start_scrapping(self):
        """
        Starts the scrapping process.
        """
        self.drone_track_entity = self.scrapper_controller.start_scrap_data(
            self.drone_data_file_path)

    def load_module(self):
        """
        Loads the module, initializes the scrapped data and syncronizes video input.
        """
        self.start_scrapping()
        self.drone_track_entity.set_input_video(self.drone_video_file_path)
