import sys
import os
from functools import partial
from PyQt5 import QtCore

# from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QVBoxLayout
from PyQt5 import QtWidgets


class Dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        mainLayout = QtWidgets.QVBoxLayout()

        # ------------ QPushButton ---------------------------
        helloButton = QtWidgets.QPushButton("Hello QT World")
        byeButton = QtWidgets.QPushButton("Bye Bye QT World")

        # ------------ Connections ---------------------------
        helloButton.clicked.connect(self.greetings)
        byeButton.clicked.connect(partial(self.sayBye, " Qt"))

        # ------------ mainLayout ----------------------------
        mainLayout.addWidget(helloButton)
        mainLayout.addWidget(byeButton)

        self.setLayout(mainLayout)
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Basic Layouts")

    def greetings(self):
        print("You clicked Hello")

    def sayBye(self, input):
        print("Bye Bye {}".format(input))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
