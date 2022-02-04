import os
import pickle
from pandas import DataFrame
import numpy as np
import cv2
import logging
import argparse


def load_model(model_dir):
    model_filepath = os.path.join(model_dir, 'model_scikit.pickle')

    with open(model_filepath, 'rb') as fid:
        model = pickle.load(fid)

    return model


class SkinDetector:
    def __init__(self, model_dir):
        self.model = load_model(model_dir)
        labels_file = os.path.join(model_dir, 'labels.pickle')
        self.labels = pickle.loads(open(labels_file, "rb").read())

    def detect_skin(self, img):
        mask = self.get_skin_mask(img)
        skin = np.multiply(img, mask)
        return skin

    def get_skin_mask(self, img):
        img_height, img_width, num_channels = img.shape
        img = img.reshape((img_height * img_width, num_channels))
        pixels = DataFrame(img, columns=['b', 'g', 'r'])
        mask = np.array(self.model.predict(pixels), dtype=np.uint8)
        mask = mask.reshape((img_height, img_width, 1))

        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((10, 10), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = mask.reshape((img_height, img_width, 1))
        return mask

    def is_skin(self, b, g, r):
        pixel = DataFrame([[b, g, r]], columns=['b', 'g', 'r'])
        probs = self.model.predict(pixel)[0]
        return probs


def convert_ds_to_skin_detected(ds_dir, new_ds_dir):
    det = SkinDetector('pretrained')

    classes = os.listdir(ds_dir)

    for c in classes:
        class_dir = os.path.join(ds_dir, c)
        new_class_dir = os.path.join(new_ds_dir, c)

        if not os.path.isdir(new_class_dir):
            os.mkdir(new_class_dir)
            logging.info('Created directory %s' % new_class_dir)

        images = os.listdir(class_dir)

        for num, img_name in enumerate(images):
            img_path = os.path.join(class_dir, img_name)
            img_new_path = os.path.join(new_class_dir, img_name)

            img = cv2.imread(img_path)
            cv2.imwrite(img_new_path, det.detect_skin(img))

            if num % 100 == 0:
                logging.info('Converted %s of %s images for class %s' % (num, len(images), c))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset', type=str, help='Directory for the images used for training.')
    parser.add_argument('output_dataset', type=str, help='Output dataset directory')
    args = parser.parse_args()

    if not os.path.isdir(args.output_dataset):
        os.mkdir(args.output_dataset)
        logging.info('Created directory %s' % args.output_dataset)

    convert_ds_to_skin_detected(args.dataset, args.output_dataset)
