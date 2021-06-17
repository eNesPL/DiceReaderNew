from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel

import DiceReader as dr
import threading
from Server import Server
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Button_DiceRead = QtWidgets.QPushButton(self.centralwidget)
        self.Button_DiceRead.setGeometry(QtCore.QRect(320, 230, 161, 41))
        self.Button_DiceRead.setObjectName("Button_DiceRead")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(310, 80, 181, 91))
        self.lcdNumber.setObjectName("lcdNumber")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.Button_DiceRead.clicked.connect(self.ReadDice)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Button_DiceRead.setText(_translate("MainWindow", "Read Dice"))

    def ReadDice(self):

        v = dr.readDice()
        self.lcdNumber.display(v)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    s = Server()
    threading.Thread(target = s.Start).start()
    threading.Thread(target = s.Broadcast).start()
    sys.exit(app.exec_())

