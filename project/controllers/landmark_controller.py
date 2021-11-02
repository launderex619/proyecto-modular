from typing import List
from entities.landmark_entity import LandmarkEntity
from entities.point_3d_entity import Point3DEntity


class LandmarkController:

    def __init__(self):
        self.landmarks: List[LandmarkEntity] = []
        self.lastTag = 0

    def update_landmark_position(self, landmark: LandmarkEntity, point: Point3DEntity):
        '''
        Agrega un nuevo punto al landmark dado
        :param landmark: LandmarkEntity
        :param point: Point3DEntity
        :return: void
        '''
        landmark.points.append(Point3DEntity)

    def get_landmark_by_tag(self, tag) -> LandmarkEntity or None:
        '''
        Devuelve el landmark en caso de existir el tag, en caso contrario, se regresa NONE
        :param tag: str
        :return: LandmarkEntity | None
        '''
        for landmark in self.landmarks:
            if landmark.tag == tag:
                return landmark
        return None

    def get_landmark_by_point(self, point: Point3DEntity) -> LandmarkEntity or None:
        '''
        Devuelve el landmark en caso de existir el punto, en caso contrario, se regresa NONE
        :param point: Point3DEntity
        :return: LandmarkEntity | None
        '''
        for landmark in self.landmarks:
            if LandmarkEntity.points_are_equal(landmark.points[-1], point):
                return landmark
        return None

    def set_landmark(self, landmark: LandmarkEntity):
        '''
        Agrega un nuevo landmark a la lista de landmarks
        :param landmark: LandmarkEntity
        :return: void
        '''
        self.landmarks.append(landmark)

    def update_landmarks(self, frame_counter: int, matches: List[object], last_frame_keypoints: List[object], keypoints: List[object]):
        '''
        Actualiza las posiciones de los landmarks encontrados
        :param frame_counter: int
        :param matches: matches
        :param last_frame_keypoints: keypoints
        :param keypoints: keypoints
        :return: void
        '''
        if len(self.landmarks) > 0:
            # Validar que el landmark recivido exita en previos frames
            for m in matches:
                x = int(last_frame_keypoints[m[0].queryIdx].pt[0])
                y = int(last_frame_keypoints[m[0].queryIdx].pt[1])
                z = 0
                point = Point3DEntity(frame_counter, x, y, z)
                landmark = self.get_landmark_by_point(point)
                if landmark is not None:
                    x = int(keypoints[m[0].trainIdx].pt[0])
                    y = int(keypoints[m[0].trainIdx].pt[1])
                    z = 0
                    point = Point3DEntity(frame_counter, x, y, z)
                    landmark.points.append(point)
                else:
                    x = int(keypoints[m[0].trainIdx].pt[0])
                    y = int(keypoints[m[0].trainIdx].pt[1])
                    z = 0
                    point = Point3DEntity(frame_counter, x, y, z)
                    landmark = LandmarkEntity(str(self.lastTag), [point])
                    self.landmarks.append(landmark)
                    self.lastTag += 1

        else:
            for m in matches:
                x = int(keypoints[m[0].trainIdx].pt[0])
                y = int(keypoints[m[0].trainIdx].pt[1])
                z = 0
                point = Point3DEntity(frame_counter, x, y, z)
                landmark = LandmarkEntity(str(self.lastTag), [point])
                self.landmarks.append(landmark)
                self.lastTag += 1

    def get_points_by_frame(self, frame) -> List[Point3DEntity]:
        points = []
        for landmark in self.landmarks:
            for point in landmark.points:
                if point.frame_number == frame:
                    points.append(point)
                    continue
        return points
