from project.entities.point_3d_entity import Point3DEntity


class LandmarkEntity:

    def __init__(self, tag: str, points):
        self.tag: str = tag
        self.points: [Point3DEntity] = points

    @staticmethod
    def points_are_equal(point1: Point3DEntity, point2: Point3DEntity) -> bool:
        if point1.x != point2.x:
            return False
        if point1.y != point2.y:
            return False
        if point1.z != point2.z:
            return False
        return True
