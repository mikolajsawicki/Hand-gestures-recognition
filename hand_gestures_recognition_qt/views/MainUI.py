from PyQt5.QtWidgets import QMainWindow, QStatusBar, QToolBar, QVBoxLayout, QLabel, QWidget
from PyQt5.QtMultimediaWidgets import QCameraViewfinder


class MainUI(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('QMainWindow')
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

        self.cameraDisplay = QCameraViewfinder()
        self.cameraDisplay.show()

        self.gestureLabel = QLabel('No gesture detected yet.')

        self.centralLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.centralLayout)

        self.centralLayout.addWidget(self.cameraDisplay)
        self.centralLayout.addWidget(self.gestureLabel)

        self.showFullScreen()


    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('Exit', self.close)


    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)


    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Everything's fine...")
        self.setStatusBar(status)


