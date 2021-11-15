
import numpy as np
import math as m
import cv2 as cv
import glob
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from core import config
from controllers import tracking_controller
from modules import image_module
from project.utils import console_print_functions as cprint
from project.modules.vision import vision_module as vm


class System:
    """
    Start point from all monoslam functions, calls and methods.
    """

    def __init__(self):
        """
        Initialize the system.
        """
        self.vision_module = vm.VisionModule()
        self.object_points = (0, 0, 0)
        # self._path = config.PROJECT_PATH + '/proyecto-modular/project/assets/video/calibracion.mp4'
        self.mtx = None
        self.dist = None

    def run(self):
        """
        Start the system.
        """
        cprint.print_string("Starting system")
        # self.calibrate_camera() TODO: this function
        self.vision_module.start_analysis()


def init():
    """
    Initialize the system.
    """
    cprint.print_welcolme()
    system = System()
    system.run()
