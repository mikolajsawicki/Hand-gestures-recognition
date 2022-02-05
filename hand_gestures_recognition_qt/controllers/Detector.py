from PyQt5.QtCore import QObject
import numpy as np
from hand_gestures_recognition.mediapipe.MPGestureRecognition import MPGestureRecognition


class Detector(QObject):
    def __init__(self):
        super().__init__()
        self._recognition = MPGestureRecognition()
        self._available = True

    def recogniseImage(self, img: np.ndarray):
        if self._available:
            self._available = False
            rec = self._recognizeImage(img)
            self._available = True
            return rec

        return None


    def _recognizeImage(self, img: np.ndarray):
        rec = self._recognition.recognize(img, get_image_output=False)

        if rec:
            rec_dict = rec
            rec_dict = {lab: prob for lab, prob in rec_dict.items() if prob > 0.4}
            if rec_dict:
                lab = max(rec_dict, key=rec_dict.get)
                return lab

        return None

    def available(self):
        return self._available

    def flush(self):
        pass
