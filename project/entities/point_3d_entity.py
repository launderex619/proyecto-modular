class Point3DEntity:
    def __init__(self, x: int, y: int, z: int, frame_number: int):
        self.frame_number: int = frame_number
        self.x: int = x
        self.y: int = y
        self.z: int = z

