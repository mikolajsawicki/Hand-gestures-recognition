import cv2
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import numpy as np


class Camera(QObject):
    finished = pyqtSignal()
    imageCaptured = pyqtSignal(np.ndarray)

    def __init__(self, camera_id=0):
        super().__init__()
        self._camera_id = camera_id
        self._vc = None
        self._running = False

    def start(self):
        self._running = True
        self._vc = cv2.VideoCapture(self._camera_id)

        if not self._vc.isOpened():
            msg_box = QMessageBox()
            msg_box.setText("Failed to open camera: %s." % self._camera_id)

        while self._running:
            rval, frame = self._vc.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.imageCaptured.emit(frame)
            QThread.msleep(30)

        self._vc.release()
        self.finished.emit()

    def stop(self):
        self._running = False

    def flush(self):
        pass
