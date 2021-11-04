from project.entities.input_drone_data import drone_track_entity as dte
from project.entities.input_drone_data import drone_entity as de

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

    def start_scrap_data_db(self, data_file_path: str) -> dte.DroneTrackEntity:
        """
        This method scraps all data in the db file and returns a list of all the data.
        """

        drone_track_entity = dte.DroneTrackEntity()
        self.chunks_of_raw_data = self.get_chunks_of_raw_data(
            data_file_path)
        self.chunks_of_raw_data = self.filter_bad_chunks_of_raw_data(
            self.chunks_of_raw_data)
        for chunk in self.chunks_of_raw_data:
            drone_entity = self.get_drone_entity_from_chunk(chunk)
            # TODO: Check if drone_entity is valid
            if drone_entity.is_valid():
                drone_track_entity.add_drone_entity(drone_entity)
        self.number_of_chunks = len(drone_track_entity.drone_entities)
        drone_track_entity.set_start_time(
            drone_track_entity.get_drone_entity_at_index(0).time)
        drone_track_entity.set_end_time(
            drone_track_entity.get_drone_entity_at_index(self.number_of_chunks - 1).time)

        return drone_track_entity

    def get_chunks_of_raw_data(self, data_file_path: str) -> List[List[str]]:
        """
        This method scraps the file, and gets the lines of each second and puts them into
        chunk_of_data variable wich is a list of strings.
        """
        chunks_of_raw_data = []
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
                        previus_timestamp = current_timestamp
                        current_chunk = []
        return chunks_of_raw_data

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

    def filter_bad_chunks_of_raw_data(self, chunks_of_raw_data: List[List[str]]) -> List[List[str]]:
        """
        This method filters the chunks of raw data removing bad inputs.
        """
        chunks_of_raw_data_filtered = []
        for chunk in chunks_of_raw_data:
            if self.is_valid_chunk(chunk):
                chunks_of_raw_data_filtered.append(chunk)
        return chunks_of_raw_data_filtered

    def is_valid_chunk(self, chunk: List[str]) -> bool:
        """
        This method checks if the chunk is valid to put into the drone track entity.
        """
        NUBER_OF_LINES_IN_CHUNK_TO_BE_VALID = 3
        if len(chunk) < NUBER_OF_LINES_IN_CHUNK_TO_BE_VALID:
            return False
        return True

    def get_drone_entity_from_chunk(self, chunk: List[str]) -> de.DroneEntity:
        """
        This method iterates trough the chunk and returns a drone entity from its data.
        """
        drone_entity = de.DroneEntity()
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
        if part_to_analyze.startswith('功能字8B'):
            return True
        if part_to_analyze.startswith('功能字8C'):
            return True
        if part_to_analyze.startswith('功能字9B'):
            return True
        if part_to_analyze.startswith('飞机坐标'):
            return True
        if part_to_analyze.startswith('单位类型'):
            return True
        return False

    def get_type_of_information_contained_in_line(self, line: str) -> str:
        """
        This method returns the type of information contained in the line.
        """
        part_to_analyze = line.split('   ')[1]
        if part_to_analyze.startswith('功能字8B'):
            return 'LGPlaneHyBean'
        elif part_to_analyze.startswith('功能字8C'):
            return 'LGPlaneGpsBean'
        elif part_to_analyze.startswith('功能字9B'):
            return 'SJHyInfo9BBean'
        elif part_to_analyze.startswith('飞机坐标'):
            return 'LGPlaneInfoCoords'
        else:  # 单位类型
            return 'LGPlaneInfoMoovent'

    def get_drone_entities_from_line(self, line_type: str, line: str, drone_entity: de.DroneEntity) -> de.DroneEntity:
        """
        This method returns a drone entity from the line.
        """
        if line_type == 'LGPlaneHyBean':
            drone_entity = self.get_drone_props_lg_plane_hy_bean(
                line, drone_entity)
        elif line_type == 'LGPlaneGpsBean':
            drone_entity = self.get_drone_props_lg_plane_gps_bean(
                line, drone_entity)
        elif line_type == 'SJHyInfo9BBean':
            drone_entity = self.get_drone_props_sj_hy_info_9b_bean(
                line, drone_entity)
        elif line_type == 'LGPlaneInfoCoords':
            drone_entity = self.get_drone_props_lg_plane_info_coords(
                line, drone_entity)
        else:  # LGPlaneInfoMoovent
            drone_entity = self.get_drone_props_lg_plane_info_moovement(
                line, drone_entity)
        return drone_entity

    def get_drone_props_lg_plane_hy_bean(self, line: str, drone_entity: de.DroneEntity) -> de.DroneEntity:
        """
        This method returns the drone props from the line defined as LGPlaneHyBean.

            example of line:
                19:01:52   功能字8B:LGPlaneHyBean{AttitudeRoll=103, AttitudePitch=-590, AttitudeYaw=-17643, InsInitOk=1, BaroInitOk=1, MagInitOk=1, GpsInitOk=1, FlowInitOk=0, InsCalib=1, MagXYCalib=1, MagZCalib=1, CalibProgress=0, BatVal=120, LowBat=0, TempOver=0, CurrOver=0, Armed=2, FlyMode=0, GoHomeStatu=0, Photo=0, Camera=1, VideoOn=1, Takeoff=0, AutoLand=0, LandFinish=1, GpsNum=13, GpsFine=1, GpsQuality=100, modeGps=1, RcFastMode=1, PTZadj=0}

        :param line: the line to analyze
        :param drone_entity: the drone entity to update
        :return: the drone entity
        """
        lines = line.split('   ')
        drone_entity.time = lines[0]
        lines = lines[1].removeprefix('功能字8B:LGPlaneHyBean{').split(', ')
        drone_entity.attitude_roll = float(
            lines[0].removeprefix('AttitudeRoll='))
        drone_entity.attitude_pitch = float(
            lines[1].removeprefix('AttitudePitch='))
        drone_entity.attitude_yaw = float(
            lines[2].removeprefix('AttitudeYaw='))
        return drone_entity

    def get_drone_props_lg_plane_gps_bean(self, line: str, drone_entity: de.DroneEntity) -> de.DroneEntity:
        """
        This method returns the drone props from the line defined as LGPlaneGpsBean.

            example of line:
                19:01:51   功能字8C:LGPlaneGpsBean{AirplaneLon=-1.03349728E9, AirplaneLat=2.07290432E8, Altitude=1007, Distance=0, Speed=0, Velocity=0}

        :param line: the line to analyze
        :param drone_entity: the drone entity to update
        :return: the drone entity
        """
        lines = line.split('   ')
        drone_entity.time = lines[0]
        line = lines[1].removeprefix('功能字8C:LGPlaneGpsBean')
        lines = line.removesuffix('}\n').split(', ')
        drone_entity.altitude = float(lines[2].removeprefix('Altitude='))
        drone_entity.speed = float(lines[4].removeprefix('Speed='))
        drone_entity.velocity = float(lines[5].removeprefix('Velocity='))
        return drone_entity

    def get_drone_props_sj_hy_info_9b_bean(self, line: str, drone_entity: de.DroneEntity) -> de.DroneEntity:
        """
        This method returns the drone props from the line defined as SJHyInfo9BBean.

            example of line:
                19:01:52   功能字9B:SJHyInfo9BBean{Acc=[99, 37, 978], Gyr=[-1, -5, -2], Mag=[-243, 18, -513], baro=16, ImuTemp=37, BaroTemp=39, Roll=127, Pitch=127, Thor=127, Yaw=127, Motor=[1541, 1657, 1553, 1685]}

        :param line: the line to analyze
        :param drone_entity: the drone entity to update
        :return: the drone entity
        """
        lines = line.split('   ')
        drone_entity.time = lines[0]
        line = lines[1].removeprefix('功能字9B:SJHyInfo9BBean')
        lines = line.removesuffix('}\n').split(', ')
        drone_entity.acc = [float(lines[0].removeprefix('{Acc=[')), float(
            lines[1]), float(lines[2].removesuffix(']'))]
        drone_entity.gyr = [float(lines[3].removeprefix('Gyr=[')), float(
            lines[4]), float(lines[5].removesuffix(']'))]
        drone_entity.mag = [float(lines[6].removeprefix('Mag=[')), float(
            lines[7]), float(lines[8].removesuffix(']'))]
        drone_entity.baro = float(lines[9].removeprefix('baro='))
        drone_entity.imu_temp = float(lines[10].removeprefix('ImuTemp='))
        drone_entity.baro_temp = float(lines[11].removeprefix('BaroTemp='))
        drone_entity.roll = float(lines[12].removeprefix('Roll='))
        drone_entity.pitch = float(lines[13].removeprefix('Pitch='))
        drone_entity.thor = float(lines[14].removeprefix('Thor='))
        drone_entity.yaw = float(lines[15].removeprefix('Yaw='))
        drone_entity.motors = [float(lines[16].removeprefix('Motor=[')), float(
            lines[17]), float(lines[18]), float(lines[19].removesuffix(']'))]
        return drone_entity

    def get_drone_props_lg_plane_info_coords(self, line: str, drone_entity: de.DroneEntity) -> de.DroneEntity:
        """
        This method returns the drone props from the line defined as LGPlaneInfoMoovent.

            example of line:
                19:01:52   飞机坐标[-103.3497314453125 , 20.72904396057129]  gps信号:13  角度:183.57°  前后倾斜角度:-5.9°  左右倾斜角度:1.03°  手机gps信息:坐标:[-103.34973666666669 , 20.728975] 精度:1.7

        :param line: the line to analyze
        :param drone_entity: the drone entity to update
        :return: the drone entity
        """
        lines = line.split('   ')
        drone_entity.time = lines[0]
        line = lines[1].removeprefix('飞机坐标')
        lines = line.split('  ')
        lon_lat = lines[0].split('[')[1].split(']')[0].split(',')
        drone_entity.lon = float(lon_lat[0])
        drone_entity.lat = float(lon_lat[1])
        drone_entity.gps_signal = float(lines[1].split(':')[1])
        drone_entity.angle = float(lines[2].split(':')[1].removesuffix('°'))
        drone_entity.front_rear_tilt_angle = float(
            lines[3].split(':')[1].removesuffix('°'))
        drone_entity.left_right_tilt_angle = float(
            lines[4].split(':')[1].removesuffix('°'))
        drone_entity.error = float(lines[5].split('精度:')[1].removesuffix('\n'))
        return drone_entity

    def get_drone_props_lg_plane_info_moovement(self, line: str, drone_entity: de.DroneEntity) -> de.DroneEntity:
        """
        This method returns the drone props from the line defined as LGPlaneInfoMoovement.

            example of line:
                19:01:52   单位类型：15   D:0.0 H:0.9 DS:0.0 VS:0.0

        :param line: the line to analyze
        :param drone_entity: the drone entity to update
        :return: the drone entity
        """
        lines = line.split('   ')
        drone_entity.time = lines[0]

        if (drone_entity.d == None):
            drone_entity.d = [float(lines[2].split(' ')[0].split(':')[1])]
        else:
            drone_entity.d.append(float(lines[2].split(' ')[0].split(':')[1]))
        if (drone_entity.h == None):
            drone_entity.h = [float(lines[2].split(' ')[1].split(':')[1])]
        else:
            drone_entity.h.append(float(lines[2].split(' ')[1].split(':')[1]))
        if (drone_entity.ds == None):
            drone_entity.ds = [float(lines[2].split(' ')[2].split(':')[1])]
        else:
            drone_entity.ds.append(float(lines[2].split(' ')[2].split(':')[1]))
        if (drone_entity.vs == None):
            drone_entity.vs = [float(lines[2].split(' ')[3].split(':')[1])]
        else:
            drone_entity.vs.append(float(lines[2].split(' ')[3].split(':')[1]))
        return drone_entity
