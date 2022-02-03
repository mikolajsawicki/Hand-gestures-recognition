from .CameraController import CameraController
# from hand_gestures_recognition.mediapipe.MPGestureRecognition import MPGestureRecognition
from PyQt5.QtGui import QImage
from .utils import qimage_to_numpy


class MainController:

    def __init__(self, view):
        self._view = view
        self._cameraController = CameraController(self._view.cameraDisplay, self._recognize_image)

    def _recognize_image(self, qimg: QImage):
        img = qimage_to_numpy(qimg)
