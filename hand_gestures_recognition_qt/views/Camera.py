from PyQt5.QtMultimedia import QCameraInfo, QCamera, QCameraImageCapture
from .utils import error


class Camera:
    def __init__(self, viewfinder):
        self.viewfinder = viewfinder
        self._initCamera()
        self.camera = QCamera(self.available_cameras[0])
        self.camera.setViewfinder(self.viewfinder)
        self._startCamera(self.camera)


    def _initCamera(self):
        # TODO: add chosing camera
        self.available_cameras = QCameraInfo.availableCameras()
        if not self.available_cameras:
            self.alert('No camera detected.')


    def _startCamera(self, camera: QCamera) -> None:
        camera.setCaptureMode(QCamera.CaptureStillImage)
        camera.error.connect(lambda: error(camera.errorString()))
        camera.start()
        capture = QCameraImageCapture(camera)
        capture.error.connect(lambda error_msg, error, msg: error(msg))
