import sys
import os
from functools import partial
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from modules import widgetStyleSheet

# QModelView using QStringListModel

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        listContents = ['Liverpool','Leicester','Man City','Chelsea']
        listModel = QtCore.QStringListModel(listContents)        

        # ------------ QListWidget ----------------------------
        leftListView = QtWidgets.QListView()
        rightListView = QtWidgets.QListView()

        leftListView.installEventFilter(self)
        rightListView.installEventFilter(self)

        leftListView.setModel(listModel)
        rightListView.setModel(listModel)

        # ------------ QComboBox ------------------------------
        comboBox = QtWidgets.QComboBox()
        comboBox.setModel(listModel)

        # ------------ QPushButton ----------------------------
        debugPushButton = QtWidgets.QPushButton('Debug')
        addPushButton = QtWidgets.QPushButton('Add Item')
        removePushButton = QtWidgets.QPushButton('Remove Item')

        # ------------ rightLayout ----------------------------
        rightLayout = QtWidgets.QVBoxLayout()
        rightLayout.addWidget(rightListView)
        rightLayout.addWidget(comboBox)

        # ------------ topLayout -----------------------------
        topLayout = QtWidgets.QHBoxLayout()
        topLayout.setAlignment(QtCore.Qt.AlignLeft)            
        topLayout.addWidget(leftListView)
        topLayout.addLayout(rightLayout)

        # ------------ bottomLayout ---------------------------
        bottomLayout = QtWidgets.QHBoxLayout()
        bottomLayout.addWidget(debugPushButton)
        bottomLayout.addWidget(addPushButton)
        bottomLayout.addWidget(removePushButton)

        # ------------ mainLayout -----------------------------
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)

        # ------------ Connections ----------------------------
        debugPushButton.clicked.connect(partial(self.debug,listModel))
        addPushButton.clicked.connect(partial(self.addItem,listModel))
        removePushButton.clicked.connect(partial(self.removeItem,leftListView,listModel))

        # ------------ mainWidget -----------------------------
        mainWidget = QtWidgets.QWidget()
        mainWidget.setLayout(mainLayout)

        self.setMinimumSize(400, 100)
        self.setWindowTitle("QModelView Sample 1")
        self.setCentralWidget(mainWidget)
        self.show()

    def debug(self,listModel):
        print(listModel.stringList())

    def addItem(self,listModel=QtCore.QStringListModel()):
        stringQVariant = QtCore.QVariant('New Club')
        row = listModel.rowCount()

        listModel.insertRow(row)
        listModel.setData(listModel.index(row),stringQVariant)

    def removeItem(self,leftView,listModel=QtCore.QStringListModel()):
        selectedIndexes = leftView.selectedIndexes()
        if selectedIndexes:
            currentRow = selectedIndexes[0].row()
            listModel.removeRow(currentRow)

        leftView.clearSelection()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec_())