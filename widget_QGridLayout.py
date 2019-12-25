import sys
import os
from functools import partial
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from modules import widgetStyleSheet

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        # ------------ QPushButton ----------------------------
        buttonA = QtWidgets.QPushButton(" A ")
        buttonB = QtWidgets.QPushButton(" B ")
        buttonC = QtWidgets.QPushButton(" C ")
        buttonD = QtWidgets.QPushButton(" D ")
        buttonE = QtWidgets.QPushButton(" E ")
        buttonF = QtWidgets.QPushButton(" F ")
        buttonG = QtWidgets.QPushButton(" G ")
        buttonH = QtWidgets.QPushButton(" H ")
        buttonI = QtWidgets.QPushButton(" I ")

        # ------------ gridLayout -----------------------------
        gridLayout = QtWidgets.QGridLayout()
        gridLayout.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        gridLayout.setAlignment(QtCore.Qt.AlignTop)
        gridLayout.setSpacing(0)
        gridLayout.setColumnStretch(0,1)
        gridLayout.setColumnStretch(1,2)
        gridLayout.setColumnStretch(2,1)
        gridLayout.setRowMinimumHeight(2,50)

        gridLayout.addWidget(buttonA,0,0)
        gridLayout.addWidget(buttonB,0,1)
        gridLayout.addWidget(buttonC,0,2)
        gridLayout.addWidget(buttonD,1,0)
        gridLayout.addWidget(buttonE,1,1)
        gridLayout.addWidget(buttonF,1,2)
        gridLayout.addWidget(buttonG,2,0)
        gridLayout.addWidget(buttonH,2,1)
        gridLayout.addWidget(buttonI,2,2)

        # ------------ mainWidget -----------------------------
        mainWidget = QtWidgets.QWidget()
        mainWidget.setStyleSheet(widgetStyleSheet.widgetMain)
        mainWidget.setLayout(gridLayout)

        self.setMinimumSize(400, 100)
        self.setWindowTitle("QGridLayout Sample")
        self.setCentralWidget(mainWidget)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec_())