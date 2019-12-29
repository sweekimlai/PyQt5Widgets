import sys
import os
import random
from functools import partial
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from modules import widgetStyleSheet

movieTitleList = ['Jumanji','Dark Knight','Narnia','Harry Potter','Apes','Hobbits','Rampage']

class CommandAdd(QtWidgets.QUndoCommand):

    def __init__(self, listWidget, row, string, description):
        super(CommandAdd, self).__init__(description)
        self.listWidget = listWidget
        self.row = row
        self.string = string

    def redo(self):
        self.listWidget.insertItem(self.row, self.string)
        self.listWidget.setCurrentRow(self.row)

    def undo(self):
        item = self.listWidget.takeItem(self.row)
        del item

class CommandDelete(QtWidgets.QUndoCommand):
    def __init__(self, listWidget, item, row, description):
        super(CommandDelete, self).__init__(description)
        self.listWidget = listWidget
        self.string = item.text()
        self.row = row

    def redo(self):
        item = self.listWidget.takeItem(self.row)
        del item

    def undo(self):
        self.listWidget.insertItem(self.row, self.string)

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        # ------------ QUndoStack -----------------------------
        self.undoStack = QtWidgets.QUndoStack(self)
        self.stackview = QtWidgets.QUndoView(self.undoStack)

        # ------------ QLabel ---------------------------------
        undoHistoryLabel = QtWidgets.QLabel('Undo History')

        # ------------ QPushButton ----------------------------
        addPushButton = QtWidgets.QPushButton("Add Movie")
        removePushButton = QtWidgets.QPushButton("Remove Movie")
        editPushButton = QtWidgets.QPushButton("Edit Movie")
        sortPushButton = QtWidgets.QPushButton("Sort Movie")
        undoPushButton = QtWidgets.QPushButton("Undo")
        redoPushButton = QtWidgets.QPushButton("Redo")

        addPushButton.setFixedWidth(150)

        # ------------ QListWidget ----------------------------
        movieList = QtWidgets.QListWidget()
        movieList.addItems(movieTitleList)

        # ------------ Buttons Layout -------------------------
        buttonsLayout = QtWidgets.QVBoxLayout()
        buttonsLayout.setAlignment(QtCore.Qt.AlignBottom)
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(addPushButton)
        buttonsLayout.addWidget(removePushButton)
        buttonsLayout.addWidget(editPushButton)
        buttonsLayout.addWidget(sortPushButton)
        buttonsLayout.addWidget(undoPushButton)
        buttonsLayout.addWidget(redoPushButton)

        # ------------ Undo Stack Layout ----------------------
        undoStackLayout = QtWidgets.QVBoxLayout()
        undoStackLayout.addWidget(undoHistoryLabel)
        undoStackLayout.addWidget(self.stackview)

        # ------------ mainLayout -----------------------------
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignLeft)
        mainLayout.setSpacing(10)
        mainLayout.addWidget(movieList)
        mainLayout.addLayout(buttonsLayout)

        # ------------ Connections ----------------------------
        addPushButton.clicked.connect(partial(self.addMovie,movieList))
        removePushButton.clicked.connect(partial(self.removeMovie,movieList))
        undoPushButton.clicked.connect(self.undoStack.undo)
        redoPushButton.clicked.connect(self.undoStack.redo)

        # ------------ undoStackWidget ------------------------
        undoStackWidget = QtWidgets.QWidget()
        undoStackWidget.setLayout(undoStackLayout)

        # ------------ mainWidget -----------------------------
        mainWidget = QtWidgets.QWidget()
        mainWidget.setLayout(mainLayout)

        # ------------ QSplitter ------------------------------
        mainSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        mainSplitter.setHandleWidth(10)
        mainSplitter.addWidget(undoStackWidget)
        mainSplitter.addWidget(mainWidget)
        mainSplitter.setSizes([10,200])
        mainSplitter.setStyleSheet(widgetStyleSheet.hSplitterStyleSheet)

        self.setMinimumSize(200,600)
        self.setWindowTitle("QUndoStack Sample")
        self.setCentralWidget(mainSplitter)
        self.show()

    def addMovie(self,listWidget):
        num = random.randint(1,100)
        newMovieName = 'Star Wars Episode {}'.format(num)
        row = listWidget.count()

        command = CommandAdd(listWidget, row, newMovieName,'Add {}'.format(newMovieName))
        self.undoStack.push(command)

    def removeMovie(self,listWidget):
        row = listWidget.currentRow()
        item = listWidget.item(row)

        command = CommandDelete(listWidget, item, row,'Delete {}'.format(item.text()))
        self.undoStack.push(command)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec_())