from .JointDetection import JointDetection
import pickle
import pathlib
import numpy as np
from pandas import DataFrame


PATH_MODEL = pathlib.Path(__file__).parent.joinpath('pretrained_model').joinpath('model_random_forest.pickle')
PATH_LABELS = pathlib.Path(__file__).parent.joinpath('pretrained_model').joinpath('labels.pickle')


class MPGestureRecognition:
    def __init__(self, static_image_mode=False):
        self.joint_detection = JointDetection(static_image_mode)
        self.model = load_pickle(PATH_MODEL)
        self.gesture_labels = load_pickle(PATH_LABELS)

    def recognize(self, img: np.ndarray, get_image_output=False):
        """
        :param img: image to recognize
        :param get_image_output: if set, then returns label: prob dict + processed image
        :return: dictionary of 'gesture_label': float probability
                 If get_image_output is True, then returns a tuple of dict and processed image
        """

        ret = self.joint_detection.get_angles(img, get_image_output)
        if ret is not None:
            angles, _, image = ret
            angles = DataFrame([angles], columns=JointDetection.get_angles_labels())
            probs = self.model.predict_proba(angles)[0]
            recognitions = dict(zip(self.gesture_labels, probs))

            return (recognitions, image) if get_image_output else recognitions

        return None


def load_pickle(filepath):
    with open(filepath, 'rb') as fid:
        pick = pickle.load(fid)

    return pick
