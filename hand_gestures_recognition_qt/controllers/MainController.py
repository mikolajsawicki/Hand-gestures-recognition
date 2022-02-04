from PyQt5.QtCore import QThread, pyqtSignal, QObject
import numpy as np

from .CameraController import Camera
from hand_gestures_recognition.mediapipe.MPGestureRecognition import MPGestureRecognition
from PyQt5.QtGui import QPixmap
from .utils import numpy_to_qimage


class MainController(QObject):
    _cameraStopSignal = pyqtSignal()

    def __init__(self, view):
        super().__init__()
        self._view = view
        self._recognition = MPGestureRecognition()
        self._initCamera()

    def _initCamera(self):
        self._cameraThread = QThread()
        self._camera = Camera()
        self._cameraStopSignal.connect(self._camera.stop)
        self._camera.moveToThread(self._cameraThread)

        self._camera.finished.connect(self._cameraThread.quit)
        self._camera.finished.connect(self._camera.deleteLater)
        self._camera.imageCaptured.connect(lambda img: self._processImage(img))
        self._cameraThread.finished.connect(self._cameraThread.deleteLater)

        self._cameraThread.started.connect(self._camera.start)
        self._cameraThread.finished.connect(self._camera.stop)
        self._cameraThread.start()

    def _processImage(self, img: np.array):
        rec = self._recognizeImage(img)
        if rec is not None:
            img = rec

        qimg = numpy_to_qimage(img)
        qpix = QPixmap.fromImage(qimg)
        self._view.cameraDisplay.setPixmap(qpix)


    def _recognizeImage(self, img: np.array):
        rec = self._recognition.recognize(img, get_image_output=True)

        if rec:
            rec_dict, img = rec
            rec_dict = {lab: prob for lab, prob in rec_dict.items() if prob > 0.5}
            if rec_dict:
                lab = max(rec_dict, key=rec_dict.get)
                self._view.setGestureText(lab)
                return img

        return None


