from PyQt5.QtWidgets import QMainWindow, QStatusBar, QToolBar
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from .Camera import Camera


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('QMainWindow')
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()

        self.camera = Camera(self.viewfinder)

        # making it central widget of main window
        self.setCentralWidget(self.viewfinder)
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


