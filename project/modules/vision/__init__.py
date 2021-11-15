from project.controllers.vision import orb_controller as ob
from project.controllers.vision import matcher_controller as mc


class VisionModule:
    """
    This class is in charge of the vision operations as orb, tracking, 
    matching, etc... Related to the camera.
    """

    def __init__(self):
        self.orb = ob.ORBController()
        self.matcher = mc.MatcherController()

        pass
