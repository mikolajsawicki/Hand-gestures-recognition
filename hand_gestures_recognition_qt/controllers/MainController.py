from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
import numpy as np
from .utils import numpy_to_qimage
from .CameraController import CameraController
from .DetectorController import DetectorController
import cv2


class MainController(QObject):
    _cameraStopSignal = pyqtSignal()

    def __init__(self, view):
        super().__init__()
        self._view = view
        self._initCamera()
        self._initDetector()
        self._gesture_text = ''

    def _initCamera(self):
        self._cameraThread = QThread()
        self._camera = CameraController()
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
        self._detector = DetectorController()
        self._detector.imageDetected.connect(self._imageDetected)
        self._detectorThread = QThread()
        self._detector.moveToThread(self._detectorThread)
        self._detectorThread.start()

    def _processImage(self, img: np.array):
        if self._detector.available():
            self._detector.recogniseImage(img)

        label_pos = int(img.shape[1] * 0.2), int(img.shape[0] * 0.9)
        labeled_img = cv2.putText(img=img, text=self._gesture_text, org=label_pos, fontFace=3, fontScale=2,
                                   color=(0, 0, 255), thickness=3)

        qimg = numpy_to_qimage(labeled_img)
        qpix = QPixmap.fromImage(qimg)
        self._view.cameraDisplay.setPixmap(qpix)

    def _imageDetected(self, label, prob):
        self._gesture_text = '{} ({:.2%})'.format(label, prob)
