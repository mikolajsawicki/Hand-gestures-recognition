from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMessageBox
import numpy as np


def numpy_to_qimage(img: np.array) -> QImage:
    height, width, channel = img.shape
    bytes_per_line = 3 * width
    return QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)


def qimage_to_numpy(qimg: QImage) -> np.array:
    '''  Converts a QImage into an opencv MAT format  '''

    incomingImage = qimg.convertToFormat(QImage.Format.Format_RGB32)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.constBits()
    arr = np.array(ptr).reshape(height, width, 3)  # Copies the data
    return arr


def error(msg):
    message_box = QMessageBox()
    message_box.critical(None, "Error", msg)
    message_box.setFixedSize(500, 200)
