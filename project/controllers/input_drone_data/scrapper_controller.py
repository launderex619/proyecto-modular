from entities.input_drone_data import DroneTrackEntity
from entities.input_drone_data import DroneEntity

from typing import List, Tuple
from copy import copy

import json


class ScrapperController:
    """
    This class is responsible for the scrapping of the data retrieved from the drone application.
    """

    def __init__(self) -> None:
        self.chunks_of_raw_data = List[List]  # type: List[List[str]]
        self.number_of_chunks = 0

    def start_scrap_data(self, data_file_path: str) -> DroneTrackEntity:
        """
        This method scraps all data in the db file and returns a list of all the data.
        """

        drone_tracks_entity = DroneTrackEntity()
        # todo: implement the scrapping of the data
        self.chunks_of_raw_data, self.number_of_chunks = self.get_chunks_of_raw_data(
            data_file_path)
        for chunk in self.chunks_of_raw_data:
            pass

        return drone_tracks_entity

    def get_chunks_of_raw_data(self, data_file_path: str) -> Tuple[List[List[str]], int]:
        """
        This method scraps the file, and gets the lines of each second and puts them into
        chunk_of_data variable wich is a list of strings.
        """
        chunks_of_raw_data = []
        number_of_chunks = 0
        previus_timestamp = 'hh:mm:ss'
        with open(data_file_path, 'r') as data_file:
            current_chunk = []
            for line in data_file:
                if self.is_valid_line_to_chunk(line):
                    current_timestamp = line.split('   ')[0]
                    if current_timestamp == previus_timestamp:
                        current_chunk.append(line)
                    else:
                        chunks_of_raw_data.append(copy(current_chunk))
                        number_of_chunks += 1
                        previus_timestamp = current_timestamp
                        current_chunk = []
        return chunks_of_raw_data, number_of_chunks

    def is_valid_line_to_chunk(self, line: str) -> bool:
        """
        This method checks if the line is valid to put into the chunk raw data.
        """
        if line.startswith('\n'):
            return False
        if line.startswith('\r'):
            return False
        if line.startswith('\t'):
            return False
        if line.startswith('\r\n'):
            return False
        if line.startswith('\n\r'):
            return False
        if line.startswith('--------'):
            return False
        if line.startswith('DhcpInfo'):
            return False
        return True

    def get_drone_entity_from_chunk(self, chunk: List[str]) -> DroneEntity:
        """
        This method iterates trough the chunk and returns a drone entity from its data.
        """
        drone_entity = DroneEntity()
        for chunk_line in chunk:
            if self.is_valid_line_to_drone_entity(chunk_line):
                line_type = self.get_type_of_information_contained_in_line(
                    chunk_line)
                drone_entity = self.get_drone_entities_from_line(
                    line_type, chunk_line, drone_entity)

        return drone_entity

    def is_valid_line_to_drone_entity(self, line: str) -> bool:
        """
        This method checks if the line is valid to put into the drone entity.
        """
        part_to_analyze = line.split('   ')[1]
        if line.startswith('功能字8B'):
            return True
        if line.startswith('功能字8C'):
            return True
        if line.startswith('功能字9B'):
            return True
        if line.startswith('功能字9C'):
            return True
        if line.startswith('飞机坐标'):
            return True
        if line.startswith('单位类型'):
            return True
        return False

    def get_type_of_information_contained_in_line(self, line: str) -> str:
        """
        This method returns the type of information contained in the line.
        """
        if line.startswith('功能字8B'):
            return 'LGPlaneHyBean'
        if line.startswith('功能字8C'):
            return 'LGPlaneGpsBean'
        elif line.startswith('功能字9B'):
            return 'SJHyInfo9BBean'
        elif line.startswith('功能字9C'):
            return 'SJHyInfo9CBean'
        elif line.startswith('飞机坐标'):
            return 'LGPlaneInfoCoords'
        else:  # 单位类型
            return 'LGPlaneInfoMoovent'

    def get_drone_entities_from_line(self, line_type: str, line: str, drone_entity: DroneEntity) -> DroneEntity:
        """
        This method returns a drone entity from the line.
        """
        if line_type == 'LGPlaneHyBean':
            drone_entity = self.get_drone_props_lg_plane_hy_bean(
                line, drone_entity)
        elif line_type == 'LGPlaneGpsBean':
            pass
        elif line_type == 'SJHyInfo9BBean':
            pass
        elif line_type == 'SJHyInfo9CBean':
            pass
        elif line_type == 'LGPlaneInfoCoords':
            pass
        else:  # LGPlaneInfoMoovent
            pass
        return drone_entity

    def get_drone_props_lg_plane_hy_bean(self, line: str, drone_entity: DroneEntity) -> DroneEntity:
        """
        This method returns the drone props from the line defined as LGPlaneHyBean.

            example of line:
                19:01:52   功能字8B:LGPlaneHyBean{AttitudeRoll=103, AttitudePitch=-590, AttitudeYaw=-17643, InsInitOk=1, BaroInitOk=1, MagInitOk=1, GpsInitOk=1, FlowInitOk=0, InsCalib=1, MagXYCalib=1, MagZCalib=1, CalibProgress=0, BatVal=120, LowBat=0, TempOver=0, CurrOver=0, Armed=2, FlyMode=0, GoHomeStatu=0, Photo=0, Camera=1, VideoOn=1, Takeoff=0, AutoLand=0, LandFinish=1, GpsNum=13, GpsFine=1, GpsQuality=100, modeGps=1, RcFastMode=1, PTZadj=0}

        :param line: the line to analyze
        :param drone_entity: the drone entity to update
        :return: the drone entity
        """
        drone_entity.time = line.split('   ')[0]
        line = line.removeprefix('功能字8B:')
        json_line_data = json.loads(line)
        drone_entity.attitude_roll = json_line_data['AttitudeRoll']
        drone_entity.attitude_pitch = json_line_data['AttitudePitch']
        drone_entity.attitude_yaw = json_line_data['AttitudeYaw']
        return drone_entity
