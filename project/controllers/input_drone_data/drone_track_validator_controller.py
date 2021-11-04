from project.entities.input_drone_data.drone_track_entity import DroneTrackEntity
from project.entities.input_drone_data.json_drone_entity import JsonDroneEntity

from typing import List, Tuple
from copy import copy

import json


class DroneTrackValidatorController:
    """
    This class is responsible for validate all drone entities in the list.
    """

    def __init__(self) -> None:
        self.json_drone_entity = List[JsonDroneEntity]
        self.number_of_drone_entities = 0

    def validate_drone_track(self, drone_track_entity: DroneTrackEntity, drone_data_json_file_path: str) -> None:
        """
        This method is responsible for validate all drone entities in the list.
        :param drone_track_entity: DroneTrackEntity
        :param drone_data_json_file_path: str
        :return: None
        """
        self.json_drone_entity = self.__read_json_file(
            drone_data_json_file_path)
        self.number_of_drone_entities = len(self.json_drone_entity)
        self.__validate_drone_track_entity(drone_track_entity)
