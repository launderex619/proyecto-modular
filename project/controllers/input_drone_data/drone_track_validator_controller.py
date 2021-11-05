from project.entities.input_drone_data.drone_track_entity import DroneTrackEntity
from project.entities.input_drone_data.json_drone_entity import JsonDroneEntity

from typing import List, Tuple
from copy import copy
from datetime import datetime, timedelta

import json


class DroneTrackValidatorController:
    """
    This class is responsible for validate all drone entities in the list.
    """

    def __init__(self) -> None:
        self.json_drone_entities = List[JsonDroneEntity]

    def validate_drone_track(self, drone_track_entity: DroneTrackEntity, drone_data_json_file_path: str) -> None:
        """
        This method is responsible for validate all drone entities in the list.
        :param drone_track_entity: DroneTrackEntity
        :param drone_data_json_file_path: str
        :return: None
        """
        drone_track_entity.video_duration_secs = (
            datetime.strptime(drone_track_entity.end_time, '%H:%M:%S') -
            datetime.strptime(drone_track_entity.start_time, '%H:%M:%S')
        )
        self.json_drone_entities = self.convert_json_file_to_json_data(
            drone_data_json_file_path)
        self.merge_entities_to_drone_track(drone_track_entity)
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
        # usyng correct lat and long
        for index_i in range(drone_track_entity.get_drone_entity_count()):
            if index_i < len(self.json_drone_entities):
                drone_track_entity.drone_entities[index_i].latitude = self.json_drone_entities[index_i].lat
                drone_track_entity.drone_entities[index_i].longitude = self.json_drone_entities[index_i].lon

    def merge_entities_to_drone_track(self, drone_track_entity: DroneTrackEntity) -> None:
        """
        This method is responsible for merge entities to drone track entity.
        :param drone_track_entity: DroneTrackEntity
        :return: None
        """
        start_time = datetime.strptime(
            drone_track_entity.start_time, '%H:%M:%S')

        # cycle to add non existent elements in between data captured
        for index_i in range(drone_track_entity.get_drone_entity_count()):
            actual_time = str((start_time + timedelta(seconds=index_i)).time())
            if drone_track_entity.drone_entities[index_i].time != actual_time:
                new_drone_entity = copy(
                    drone_track_entity.drone_entities[index_i])
                new_drone_entity.time = actual_time
                drone_track_entity.drone_entities.insert(index_i,
                                                         new_drone_entity)
            drone_track_entity.drone_entities[index_i].id = index_i

        # cycles to make both lists same length
        while (drone_track_entity.get_drone_entity_count() > len(self.json_drone_entities)):
            self.json_drone_entities.insert(
                0, copy(self.json_drone_entities[0]))

        while (drone_track_entity.get_drone_entity_count() < len(self.json_drone_entities)):
            self.json_drone_entities.pop(0)
