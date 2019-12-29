import sys
import os
from functools import partial
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        # ------------ QUndoStack -----------------------------
        self.undoStack = QtWidgets.QUndoStack()

        undoAction = self.undoStack.createUndoAction(self, self.tr("&Undo"))
        undoAction.setShortcuts(QtGui.QKeySequence.Undo)
        redoAction = self.undoStack.createRedoAction(self, self.tr("&Redo"))
        redoAction.setShortcuts(QtGui.QKeySequence.Redo)

        # ------------ QLabel ---------------------------------
        nameLabel = QtWidgets.QLabel('Name:')
        addressLabel = QtWidgets.QLabel('Address:')
        emptyLabel = QtWidgets.QLabel('')

        # ------------ QPushButton ----------------------------
        undoButton = QtWidgets.QToolButton()
        undoButton.setDefaultAction(undoAction)
        redoButton = QtWidgets.QToolButton()
        redoButton.setDefaultAction(redoAction)

        # ------------ QLineEdit ------------------------------
        nameLineEdit = QtWidgets.QLineEdit()
        addressALineEdit = QtWidgets.QLineEdit()

        nameLineEdit.editingFinished.connect(self.storeFieldText)
        addressALineEdit.editingFinished.connect(self.storeFieldText)

        # ------------ QVBoxLayout ----------------------------
        addressLayout = QtWidgets.QVBoxLayout()
        addressLayout.addWidget(addressALineEdit)
        addressLayout.setSpacing(5)

        # ------------ Undo Redo Layout -----------------------
        undoRedoLayout = QtWidgets.QHBoxLayout()
        undoRedoLayout.addWidget(undoButton)
        undoRedoLayout.addWidget(redoButton)

        # ------------ FormLayout -----------------------------
        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow(nameLabel,nameLineEdit)
        formLayout.addRow(addressLabel,addressLayout)
        formLayout.addRow(emptyLabel,undoRedoLayout)
        formLayout.setSpacing(15)
        formLayout.setHorizontalSpacing(50)

        # ------------ mainWidget -----------------------------
        mainWidget = QtWidgets.QWidget()
        mainWidget.setLayout(formLayout)


        self.setMinimumSize(400, 100)
        self.setWindowTitle("QFormLayout Sample")
        self.setCentralWidget(mainWidget)
        
        addressALineEdit.setFocus()
        self.show()
    
    def storeFieldText(self):
        command = StoreCommand(self.sender())
        self.undoStack.push(command)

class StoreCommand(QtWidgets.QUndoCommand):
    def __init__(self, field):

        QtWidgets.QUndoCommand.__init__(self)

        # Record the field that has changed.
        self.field = field

        # Record the text at the time the command was created.
        self.text = field.text()

    def undo(self):
        # Remove the text from the file and set it in the field.
        # ...
        self.field.setText(self.text)

    def redo(self):
        # Store the text in the file and set it in the field.
        # ...
        self.field.setText(self.text)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec_())