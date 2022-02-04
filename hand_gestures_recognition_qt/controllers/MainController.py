from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
import numpy as np
from .utils import numpy_to_qimage
from .CameraController import Camera
from .Detector import Detector


class MainController(QObject):
    _cameraStopSignal = pyqtSignal()

    def __init__(self, view):
        super().__init__()
        self._view = view
        self._initCamera()
        self._initDetector()

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

    def _initDetector(self):
        self._detector = Detector()
        self._detectorThread = QThread()
        self._detector.moveToThread(self._detectorThread)
        self._detectorThread.start()

    def _processImage(self, img: np.array):
        if self._detector.available():
            label = self._detector.recogniseImage(img)
            if label is not None:
                self._view.setGestureText(label)

        qimg = numpy_to_qimage(img)
        qpix = QPixmap.fromImage(qimg)
        self._view.cameraDisplay.setPixmap(qpix)





