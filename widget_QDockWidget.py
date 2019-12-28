import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets

class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__()

        # ------------ QPushButton ----------------------------
        buttonA = QtWidgets.QPushButton('Button A')
        buttonB = QtWidgets.QPushButton('Button B')

        # ------------ QListWidget ----------------------------
        listWidgetA = QtWidgets.QListWidget()
        listWidgetA.addItems(['Apple','Banana','Orange','Kiwi','Papaya'])

        listWidgetB = QtWidgets.QListWidget()
        listWidgetB.addItems(['Canada','Britain','New Zealand','Singapore','Japan'])

        # ------------ Dock Layout ----------------------------
        dockLayout = QtWidgets.QVBoxLayout()
        dockLayout.setContentsMargins(4, 4, 4, 4)  # left, top, right, bottom
        dockLayout.addWidget(listWidgetA)
        dockLayout.addWidget(buttonA)
        dockLayout.addWidget(buttonB)

        # ------------ Dock Widget ----------------------------
        dockWidget = QtWidgets.QWidget()
        dockWidget.setLayout(dockLayout)

        # ------------ QDockWidget ----------------------------
        dockDemoWidget = QtWidgets.QDockWidget('Dock Demo')
        dockDemoWidget.setFeatures(dockDemoWidget.DockWidgetMovable)
        dockDemoWidget.setWidget(dockWidget)        
        dockDemoWidget.setFloating(False)

        self.setMinimumSize(600, 500)
        self.setWindowTitle("QDockWidget Sample")
        self.setCentralWidget(listWidgetB)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,dockDemoWidget)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec_())