from project.entities.landmark_entity import LandmarkEntity
from project.entities.point_3d_entity import Point3DEntity


class LandmarkController:

    def __init__(self):
        self.landmarks: [LandmarkEntity] = []

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

    def set_landmark(self, landmark: LandmarkEntity):
        '''
        Agrega un nuevo landmark a la lista de landmarks
        :param landmark: LandmarkEntity
        :return: void
        '''
        self.landmarks.append(landmark)
