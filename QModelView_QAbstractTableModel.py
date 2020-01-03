import sys
import os
import random
from functools import partial
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from modules import widgetStyleSheet

# QModelView using QAbstractTableModel

class zinTableModel(QtCore.QAbstractTableModel):
    def __init__(self,dataIn,headers,parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__data = dataIn
        self.__headers = headers

    def rowCount(self, parent= QtCore.QModelIndex()): 
        return len(self.__data)

    def columnCount(self, parent= QtCore.QModelIndex()):
        return len(self.__data[0])
 
    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            return QtCore.QVariant(self.__data[row][column])            

        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                row = index.row()
                column = index.column()
                return QtCore.QVariant(self.__data[row][column])
            elif role == QtCore.Qt.TextAlignmentRole:
                if index.column() > 0:
                    return QtCore.Qt.AlignCenter
            else: 
                return QtCore.QVariant()

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:            
            row = index.row()
            column = index.column()
            self.__data[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:            
                if section < len(self.__headers):
                    return self.__headers[section]
            else:
                return section + 1

    def getData(self):
        return self.__data
    
    def addRow(self, newData, position, rows=1, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        
        for _ in range(rows):
            self.__data.insert(position, newData)
        
        self.endInsertRows()        
        return True
    
    def removeRows(self, position, rows=1, parent = QtCore.QModelIndex()):
        # rows is set to 1 as only one item is allowed per selection
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for _ in range(rows):
            del self.__data[position]
             
        self.endRemoveRows()
        return True

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        game1 = ['Bloodborne','Action','FromSoftware','2015']
        game2 = ['BlackOps','Shooter','Treyarch','2010']
        game3 = ['Overwatch','Multiplayer','Blizzard','2016']
        game4 = ['Witcher 3','Role Playing','CD Projekt','2015']
        game5 = ['FIFA 20','Sports','Electronic Art','2019']
        game6 = ['Dirt 4','Car Racing','Codemaster','2017']
        game7 = ['Final Fantasy XV','JRPG','SquareSoft','2016']
        game8 = ['Last Of Us','Action Adventure','Naughty Dog','2013']
        game9 = ['Metal Gear Solid 5','Stealth Action','Konami','2015']
        game10 = ['Soul Calibur 5','Fighting','Bandai Namco','2012']

        self.otherGames = [game5,game6,game7,game8,game9,game10]

        gameInfo = [game1,game2,game3,game4]
        headers = ['Title','Genre','Developer','Year']

        tableModel = zinTableModel(gameInfo,headers,self)

        # ------------ QListWidget ----------------------------
        leftListView = QtWidgets.QListView()
        leftListView.setModel(tableModel)

        # ------------ QComboBox ------------------------------
        comboBox = QtWidgets.QComboBox()
        comboBox.setModel(tableModel)

        # ------------ QTableView -----------------------------
        tableView = QtWidgets.QTableView()
        tableView.setMinimumWidth(500)
        tableView.setModel(tableModel)
        tableView.setAlternatingRowColors(True)
        tableView.resizeColumnToContents(0)

        # ------------ QPushButton ----------------------------
        debugPushButton = QtWidgets.QPushButton('Debug')
        selectionPushButton = QtWidgets.QPushButton('Selection')
        addPushButton = QtWidgets.QPushButton('Add Row')
        removePushButton = QtWidgets.QPushButton('Remove Row')

        # ------------ Left Layout ----------------------------
        leftLayout = QtWidgets.QVBoxLayout()
        leftLayout.addWidget(leftListView)
        leftLayout.addWidget(comboBox)

        # ------------ Right Layout ---------------------------
        rightLayout = QtWidgets.QVBoxLayout()
        rightLayout.addWidget(tableView)

        # ------------ Controllers Layout ---------------------
        controllerLayout = QtWidgets.QVBoxLayout()
        controllerLayout.setAlignment(QtCore.Qt.AlignBottom)            
        controllerLayout.addWidget(debugPushButton)
        controllerLayout.addWidget(selectionPushButton)
        controllerLayout.addWidget(addPushButton)
        controllerLayout.addWidget(removePushButton)

        # ------------ mainLayout -----------------------------
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)
        mainLayout.addLayout(controllerLayout)

        # ------------ Connections ----------------------------
        debugPushButton.clicked.connect(partial(self.debug,tableModel))
        selectionPushButton.clicked.connect(partial(self.getSelection,tableView))
        addPushButton.clicked.connect(partial(self.addNewRow,tableModel,tableView))
        removePushButton.clicked.connect(partial(self.removeRow,tableModel,tableView))

        # ------------ mainWidget -----------------------------
        mainWidget = QtWidgets.QWidget()
        mainWidget.setLayout(mainLayout)

        self.setMinimumSize(800, 200)
        self.setWindowTitle("QAbstractTableModel Sample")
        self.setCentralWidget(mainWidget)
        self.show()

    def debug(self,tableModel):
        print(tableModel.getData())

    def getSelection(self,tableView=QtWidgets.QTableView):
        if tableView.selectionModel().selectedIndexes():
            index = tableView.selectionModel().selectedIndexes()[0]
            if index.isValid():
                modelIndex = index.sibling(index.row(),index.column())
                value = index.sibling(index.row(),index.column()).data()
                delegate = tableView.itemDelegate(modelIndex)
                print(delegate)
                #print(tableView.itemDelegateForColumn(1))
                print(value)

    def addNewRow(self,tableModel,tableView):
        num = random.randint(0,len(self.otherGames)-1)
        newData = self.otherGames[num]
        tableModel.addRow(newData = newData, position = tableModel.rowCount())
        tableView.resizeColumnToContents(0)

    def removeRow(self,tableModel,tableView):
        if tableView.selectionModel().selectedIndexes():
            index = tableView.selectionModel().selectedIndexes()[0]
            row = index.row()
            tableModel.removeRows(position=row)

        #leftView.clearSelection()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec_())