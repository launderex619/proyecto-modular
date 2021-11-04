from project.controllers.input_drone_data import scrapper_controller as sc
from project.controllers.input_drone_data import drone_track_validator_controller as dtvc


class DroneDataReceiverModule:
    """
    This class is responsible for receiving the drone data from the drone.
    """

    def __init__(self, drone_video_file_path: str, drone_data_db_file_path: str, drone_data_json_file_path: str):
        """
        Initializes the drone data receiver module.
        :param drone_info_file_path: The path of the file containing the drone information.
        """
        self.drone_video_file_path = drone_video_file_path
        self.drone_data_file_path = drone_data_db_file_path
        self.drone_data_json_file_path = drone_data_json_file_path
        self.drone_track_entity = None
        self.scrapper_controller = sc.ScrapperController()
        self.drone_track_validator_controller = dtvc.DroneTrackValidatorController()


    def start_scrapping(self):
        """
        Starts the scrapping process.
        """
        self.drone_track_entity = self.scrapper_controller.start_scrap_data_db(
            self.drone_data_file_path)
        self.drone_track_validator_controller.validate_drone_track(
            self.drone_track_entity, self.drone_data_json_file_path)
        self.sync_video_with_drone_entities()

    def sync_video_with_drone_entities(self):
        """
        Syncronizes the video with the drone entities.
        """
        """

            TODO: Crear un controlador que se encargue de lo siguiente:
                - Cargar el video en una lista de frames
                    - Asegurarse que todos los segundos realmente tengan 15 frames
                - Tomar unicamente un frame por segundo (1/fps) del video
                - Esta lista de frames asignarlas a la proiedad drone_video_frames del drone_track_entity
        """
        # fps = video.get(cv2.cv.CV_CAP_PROP_FPS)

        expe_fr = self.drone_track_entity.video_duration_secs * 15 # * fps
        real_fr = len(self.drone_track_entity.drone_video_frames)

        if expe_fr != real_fr:
            print("La cantidad es diferente")
            print(expe_fr)
            print(real_fr)

        # NOTE: for video input and ask how many frames in current second -> n
        frames = []
        for i in range(0, real_fr, 15): # n, fps
            frames.append(self.drone_track_entity.drone_video_frames[i])

        self.drone_track_entity.drone_video_frames = frames


    def load_module(self):
        """
        Loads the module, initializes the scrapped data and syncronizes video input.
        """
        self.start_scrapping()
        self.drone_track_entity.set_input_video(self.drone_video_file_path)
