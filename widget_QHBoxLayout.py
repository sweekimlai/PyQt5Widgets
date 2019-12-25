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
        helloButton = QtWidgets.QPushButton("Hello QT World")
        byeButton = QtWidgets.QPushButton("Bye Bye QT World")
        hideUnhideButton = QtWidgets.QPushButton("Hide/Unhide")
        enableDisableButton = QtWidgets.QPushButton("Enable/Disable")

        # ------------ topLayout ------------------------------
        topLayout = QtWidgets.QHBoxLayout()
        topLayout.setAlignment(QtCore.Qt.AlignLeft)
        topLayout.addWidget(helloButton)
        topLayout.addWidget(byeButton)
        topLayout.addStretch()

        # ------------ bottomLayout ---------------------------
        bottomLayout = QtWidgets.QHBoxLayout()
        bottomLayout.setAlignment(QtCore.Qt.AlignRight)
        bottomLayout.addStretch()
        bottomLayout.addWidget(hideUnhideButton)
        bottomLayout.addWidget(enableDisableButton)

        # ------------ topWidget ------------------------------
        topWidget = QtWidgets.QWidget()
        topWidget.setStyleSheet(widgetStyleSheet.widgetEnabled)
        topWidget.setLayout(topLayout)

        # ------------ bottomWidget ---------------------------
        bottomWidget = QtWidgets.QWidget()
        bottomWidget.setLayout(bottomLayout)

        # ------------ mainLayout -----------------------------
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        mainLayout.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        mainLayout.setSpacing(0)
        mainLayout.addWidget(topWidget)
        mainLayout.addWidget(bottomWidget)

        # ------------ Connections ----------------------------
        helloButton.clicked.connect(self.greetings)
        byeButton.clicked.connect(partial(self.sayBye, " Qt"))
        hideUnhideButton.clicked.connect(partial(self.hideUnhideWidget, topWidget))
        enableDisableButton.clicked.connect(partial(self.enableDisableWidget, topWidget, topLayout))

        # ------------ mainWidget -----------------------------
        mainWidget = QtWidgets.QWidget()
        mainWidget.setStyleSheet(widgetStyleSheet.widgetMain)
        mainWidget.setLayout(mainLayout)

        self.setMinimumSize(400, 100)
        self.setWindowTitle("QHBoxLayout Sample")
        self.setCentralWidget(mainWidget)
        self.show()

    def greetings(self):
        print("You clicked Hello")

    def sayBye(self, input):
        print("Bye Bye {}".format(input))

    def hideUnhideWidget(self, widget):
        if widget.isHidden():
            widget.setHidden(False)
        else:
            widget.setHidden(True)

    def enableDisableWidget(self, widget, layout):
        if widget.isEnabled():
            widget.setEnabled(False)
            widget.setStyleSheet(widgetStyleSheet.widgetDisabled)
            for i in range(layout.count()):
                w = layout.itemAt(i).widget()
                if (isinstance(w, QtWidgets.QPushButton)):                    
                    w.setFlat(True)
        else:
            widget.setEnabled(True)
            widget.setStyleSheet(widgetStyleSheet.widgetEnabled)
            for i in range(layout.count()):
                w = layout.itemAt(i).widget()
                if (isinstance(w, QtWidgets.QPushButton)):
                    w.setFlat(False)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec_())