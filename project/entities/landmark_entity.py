from project.entities.point_3d_entity import Point3DEntity


class LandmarkEntity:

    def __init__(self, tag: str, points):
        self.tag: str = tag
        self.points: Point3DEntity = points