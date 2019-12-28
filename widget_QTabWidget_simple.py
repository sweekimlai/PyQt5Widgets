import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets

class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__()

        # ------------ QPushButton ----------------------------
        buttonA = QtWidgets.QPushButton('Button A')
        buttonB = QtWidgets.QPushButton('Button B')

        # ------------ tabALayout -----------------------------
        tabALayout = QtWidgets.QVBoxLayout()
        tabALayout.addWidget(buttonA)

        # ------------ tabBLayout -----------------------------
        tabBLayout = QtWidgets.QVBoxLayout()
        tabBLayout.addWidget(buttonB)

        # ------------ QTabWidget -----------------------------
        mainTabs = QtWidgets.QTabWidget()
        tabA = QtWidgets.QWidget()
        tabB = QtWidgets.QWidget()

        tabA.setLayout(tabALayout)
        tabB.setLayout(tabBLayout)

        mainTabs.addTab(tabA,'Button A Tab A')    
        mainTabs.addTab(tabB,'Button B Tab B')

        self.setMinimumSize(600, 500)
        self.setWindowTitle("QTabWidget Sample")
        self.setCentralWidget(mainTabs)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec_())