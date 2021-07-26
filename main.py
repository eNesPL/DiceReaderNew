from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel

import DiceReader
import DiceReader as dr
import threading
from PyQt5 import QtCore, QtGui, QtWidgets

from Logic import  Ui_Logic
from DiceReader import *
import os
from Config import SaveConfig,LoadConfig,configGetUi
from Server import Server

global ui


def Close():
    os._exit(0)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Logic()
    configGetUi(ui)
    s = Server(ui)
    threading.Thread(target=s.Start).start()
    threading.Thread(target=s.Broadcast).start()
    ui.stackedWidget.setCurrentIndex(0)
    ui.GenerateCameras()
    LoadConfig()
    app.lastWindowClosed.connect(Close)
    sys.exit(app.exec_())

