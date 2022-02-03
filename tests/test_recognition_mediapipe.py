from hand_gestures_recognition.qt_app.recognition.mediapipe.MPGestureRecognition import MPGestureRecognition
import cv2
from unittest import TestCase
import pathlib


TEST_IMAGE_W = pathlib.Path(__file__).parent.joinpath('test_image_w.png')



class TestMPGestureRecognition(TestCase):

    def test_mp_gesture_recognition(self):
        img = cv2.imread(str(TEST_IMAGE_W))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_gesture_recognition = MPGestureRecognition()
        rec = mp_gesture_recognition.recognize(img)
        print(rec)
