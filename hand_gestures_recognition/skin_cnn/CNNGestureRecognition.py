from model import get_model
import numpy as np
from keras.preprocessing import image as keras_image_ops
import tensorflow as tf
import pickle
from skin_detector.SkinDetector import SkinDetector
import pathlib


PATH_MODEL = pathlib.Path(__file__).parent.joinpath('pretrained_model').joinpath('model_random_forest.pickle')
PATH_LABELS = pathlib.Path(__file__).parent.joinpath('pretrained_model').joinpath('labels.pickle')
PATH_IMAGE_SIZE = pathlib.Path(__file__).parent.joinpath('pretrained_model').joinpath('image_size.pickle')
PATH_SKIN_DETECTOR = pathlib.Path(__file__).parent.joinpath('skin_detector').joinpath('pretrained_model')


class CNNGestureRecognition:
    def __init__(self):
        self._labels = pickle.loads(open(PATH_LABELS, "rb").read())
        self._img_size = pickle.loads(open(PATH_IMAGE_SIZE, "rb").read())
        self._cnn_model = get_model(*self._img_size, len(self._labels))
        self._cnn_model.load_weights(PATH_MODEL)

        self.skin_detector = SkinDetector(PATH_SKIN_DETECTOR)


    def recognize(self, img: np.ndarray):
        img_skin = self.skin_detector.detect_skin(img)
        img_tensor = self._process_image(img_skin)

        label, prob = self._predict_image(img_tensor)

        return label, prob

    def _process_image(self, img, interpolation='bilinear', crop_to_aspect_ratio=False):
        img = tf.image.rgb_to_grayscale(img)

        if crop_to_aspect_ratio:
            img = keras_image_ops.smart_resize(img, self._img_size, interpolation=interpolation)
        else:
            img = tf.image.resize(img, self._img_size, method=interpolation)
        img.set_shape((self._img_size[0], self._img_size[1], 1))

        return img

    def _predict_image(self, img):
        imgs = np.array([img])
        preds = self._cnn_model(imgs)
        max_id = np.argmax(preds, axis=1)[0]
        predicted_label = self._labels[max_id]
        prob = preds[0][max_id].numpy()
        return predicted_label, prob


def tensor_to_numpy(tensor):
    return np.uint8(np.squeeze(tensor.numpy()))
