import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets

class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__()

        # ------------ QPushButton ----------------------------
        buttonA = QtWidgets.QPushButton('Button A')
        buttonB = QtWidgets.QPushButton('Button B')
        buttonC = QtWidgets.QPushButton('Button C')
        buttonD = QtWidgets.QPushButton('Button D')
        buttonE = QtWidgets.QPushButton('Button E')

        # ------------ QFrame ---------------------------------
        frame = QtWidgets.QFrame(self)
        frame.setLineWidth(2)
        frame.setFrameShape(QtWidgets.QFrame.Box)
        frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        frame.setStyleSheet("background-color: rgb(200,200,180);")

        # ------------ buttonLayout ---------------------------
        buttonLayout = QtWidgets.QVBoxLayout()
        buttonLayout.setSpacing(20)
        buttonLayout.addWidget(buttonA)
        buttonLayout.addWidget(buttonB)
        buttonLayout.addWidget(buttonC)
        buttonLayout.addWidget(buttonD)
        buttonLayout.addWidget(buttonE)

        # ------------ frameLayout ----------------------------
        frameLayout = QtWidgets.QVBoxLayout(frame)        
        frameLayout.addLayout(buttonLayout)

        # ------------ mainLayout -----------------------------
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.setContentsMargins(4, 4, 4, 4)  # left, top, right, bottom
        mainLayout.addWidget(frame)

        # ------------ mainWidget -----------------------------
        mainWidget = QtWidgets.QWidget()
        mainWidget.setLayout(mainLayout)

        self.setMinimumSize(200, 100)
        self.setWindowTitle("QFrame Sample")
        self.setCentralWidget(mainWidget)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec_())