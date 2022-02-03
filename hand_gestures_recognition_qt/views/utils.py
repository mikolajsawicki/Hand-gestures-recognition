from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMessageBox
import numpy as np


def numpy_to_qimage(img: np.array) -> QImage:
    height, width, channel = img.shape
    bytes_per_line = 3 * width
    return QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)


def error(msg):
    message_box = QMessageBox()
    message_box.critical(None, "Error", msg)
    message_box.setFixedSize(500, 200)
