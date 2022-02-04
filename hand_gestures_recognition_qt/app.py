import sys
from PyQt5.QtWidgets import QApplication
from views.MainView import MainView
from controllers.MainController import MainController


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.mainView = MainView()
        self.mainView.show()
        self.mainController = MainController(self.mainView)


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
