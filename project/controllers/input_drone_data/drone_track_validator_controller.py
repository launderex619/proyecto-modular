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
        self.json_drone_entities = List[JsonDroneEntity]
        self.number_of_drone_entities = 0

    def validate_drone_track(self, drone_track_entity: DroneTrackEntity, drone_data_json_file_path: str) -> None:
        """
        This method is responsible for validate all drone entities in the list.
        :param drone_track_entity: DroneTrackEntity
        :param drone_data_json_file_path: str
        :return: None
        """
        self.json_drone_entities = self.convert_json_file_to_json_data(
            drone_data_json_file_path)
        self.number_of_drone_entities = len(self.json_drone_entities)
        self.validate_drone_track_entity_data(drone_track_entity)

    def convert_json_file_to_json_data(self, drone_data_json_file_path: str) -> List[JsonDroneEntity]:
        """
        This method is responsible for convert json file to json data.
        :param drone_data_json_file_path: str
        :return: List[JsonDroneEntity]
        """
        json_data = json.load(open(drone_data_json_file_path))
        json_list = json_data.get('data')
        json_drone_entities = []
        for json_drone_entity_element in json_list:
            json_drone_entity = JsonDroneEntity()
            json_drone_entity.angle = json_drone_entity_element.get('angle')
            json_drone_entity.back = json_drone_entity_element.get('back')
            json_drone_entity.d = json_drone_entity_element.get('d')
            json_drone_entity.detail_id = json_drone_entity_element.get(
                'detail_id')
            json_drone_entity.down = json_drone_entity_element.get('down')
            json_drone_entity.font = json_drone_entity_element.get('font')
            json_drone_entity.h = json_drone_entity_element.get('h')
            json_drone_entity.hs = json_drone_entity_element.get('hs')
            json_drone_entity.id = json_drone_entity_element.get('id')
            json_drone_entity.lat = json_drone_entity_element.get('lat')
            json_drone_entity.lefrRotate = json_drone_entity_element.get(
                'lefrRotate')
            json_drone_entity.left = json_drone_entity_element.get('left')
            json_drone_entity.lon = json_drone_entity_element.get('lon')
            json_drone_entity.right = json_drone_entity_element.get('right')
            json_drone_entity.rightRotate = json_drone_entity_element.get(
                'rightRotate')
            json_drone_entity.up = json_drone_entity_element.get('up')
            json_drone_entity.vs = json_drone_entity_element.get('vs')
            json_drone_entities.append(json_drone_entity)
        return json_drone_entities

    def validate_drone_track_entity_data(self, drone_track_entity: DroneTrackEntity) -> None:
        """
        This method is responsible for validate drone track entity data.
        :param drone_track_entity: DroneTrackEntity
        :return: None
        """
        drone_track_entity_data = drone_track_entity.get_drone_track_entity_data()
        for drone_entity in drone_track_entity_data:
            self.validate_drone_entity_data(drone_entity)
