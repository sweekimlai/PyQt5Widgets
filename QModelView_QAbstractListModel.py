import sys
import os
import random
from functools import partial
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from modules import widgetStyleSheet

# QModelView using QAbstractListModel

class zinListModel(QtCore.QAbstractListModel):
    def __init__(self,listData,parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__listData = listData

    def rowCount(self, parent= QtCore.QModelIndex()): 
        return len(self.__listData)
 
    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            return QtCore.QVariant(self.__listData[index.row()])

        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.__listData[index.row()])
        else: 
            return QtCore.QVariant()

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:            
            row = index.row()
            self.__listData[row] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def stringList(self):
        return self.__listData

    def addRow(self, parent = QtCore.QModelIndex()):
        self.__listData.append('')
        return True

    def removeRows(self, position, rows=1, parent = QtCore.QModelIndex()):
        # rows is set to 1 as only one item is allowed per selection
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for _ in range(rows):
            value = self.__listData[position]
            self.__listData.remove(value)
             
        self.endRemoveRows()
        return True

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        listContents = ['Liverpool','Leicester','Man City','Chelsea']
        self.clubs = ['Arsenal','Tottenham','Wolves','Everton','Watford','Aston Villa','Southampton']
        #listModel = QtCore.QStringListModel(listContents)
        listModel = zinListModel(listContents,self)

        # ------------ QListWidget ----------------------------
        leftListView = QtWidgets.QListView()
        rightListView = QtWidgets.QListView()

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
        self.setWindowTitle("QAbstractListModel Sample")
        self.setCentralWidget(mainWidget)
        self.show()

    def debug(self,listModel):
        print(listModel.stringList())

    def addItem(self,listModel=QtCore.QStringListModel()):
        num = random.randint(0,len(self.clubs)-1)
        row = listModel.rowCount()
        listModel.addRow()
        listModel.setData(listModel.index(row),self.clubs[num])

    def removeItem(self,leftView,listModel=QtCore.QStringListModel()):
        selectedIndexes = leftView.selectedIndexes()
        if selectedIndexes:
            currentRow = selectedIndexes[0].row()
            listModel.removeRows(currentRow)

        leftView.clearSelection()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec_())