from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel
import DiceReader as dr
import threading
from PyQt5 import QtCore, QtGui, QtWidgets

from Logic import Ui_Logic
from RestApiServer import RestApiGetUi, RestApiServer, AddRoutes
from DiceReader import *
import os
from Config import SaveConfig,LoadConfig,configGetUi
global ui


def Close():
    os._exit(0)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Logic()
    configGetUi(ui)
    RestApiGetUi(ui)
    AddRoutes()
    ui.stackedWidget.setCurrentIndex(1)
    threading.Thread(target = RestApiServer).start()
    ui.GenerateCameras()
    LoadConfig()
    ui.stackedWidget.setCurrentIndex(5)
    app.lastWindowClosed.connect(Close)
    sys.exit(app.exec_())

