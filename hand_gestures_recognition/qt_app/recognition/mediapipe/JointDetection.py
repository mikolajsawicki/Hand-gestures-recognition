import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands


class JointDetection:
    def __init__(self, static_image_mode=False):
        self.mp_hands = mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )


    def get_angles(self, image: np.array, get_image_output=False):
        """
        :param image: numpy array for RGB image
        :param get_image_output: if set to True, then image with the annotations is returned
        :return: Tuple of:
        - angles array
        - points 2-dimensional numpy array
        - if get_image_output is True, then annotated image. None otherwise.

        """
        res = self.mp_hands.process(image)

        output_img = None

        if res.multi_hand_landmarks:
            if get_image_output:
                output_img = annotate_img(image.numpy(), res)

            landmark = res.multi_hand_landmarks[0].landmark

            points = np.array(np.array([p.x, p.y]) for p in landmark)
            threes = split_by_threes(points)

            angles = [angle(*t) for t in threes]

            return angles, points, output_img
        else:
            return None


    @staticmethod
    def get_angles_landmarks():
        landmarks = list(mp_hands.HandLandmark)
        return split_by_threes(landmarks)

    @staticmethod
    def get_angles_labels():
        angles_count = len(mp_hands.HandLandmark) - 2
        return [str(lab) for lab in range(angles_count)]



def angle(a, b, c):
    """
    Params
        a, b, c: numpy arrays representing points
    Return
        Angle between the three points
    """
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    y = np.arccos(cosine_angle)

    return np.degrees(y)


def split_by_threes(x):
    """

    :param x: iterable
    :return: 1-shifted threes

    Example:
        [1, 2, 3, 4, 5] => [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    """

    return [x[i: i + 3] for i in range(0, len(x) - 2)]


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def annotate_img(image, results):
    """
    :param image: numpy array
    :param results: results returned by mp_hands.process()
    :return:
    """
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
    return image
