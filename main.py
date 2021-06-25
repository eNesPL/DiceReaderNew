from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel
import DiceReader as dr
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PiUi import *
from Server import *
from DiceReader import *
from configparser import ConfigParser

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.stackedWidget.setCurrentIndex(1)
    MainWindow.show()
    s = Server()
    threading.Thread(target = s.Start).start()
    threading.Thread(target = s.Broadcast).start()
    DRGetUI(ui)
    GenerateCameras()
    ui.stackedWidget.setCurrentIndex(5)
    sys.exit(app.exec_())

