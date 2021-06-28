from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel
import DiceReader as dr
import threading
from PyQt5 import QtCore, QtGui, QtWidgets

from Logic import Ui_Logic
from Server import *
from DiceReader import *
import os
from Config import save
def Close():
    os._exit(0)
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Logic()
    ui.stackedWidget.setCurrentIndex(1)
    s = Server()
    threading.Thread(target = s.Start).start()
    threading.Thread(target = s.Broadcast).start()
    ui.GenerateCameras()
    save()
    ui.stackedWidget.setCurrentIndex(5)
    app.lastWindowClosed.connect(Close)
    sys.exit(app.exec_())

