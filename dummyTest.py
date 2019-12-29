from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5 import uic
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(366, 440)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit1.setGeometry(QtCore.QRect(130, 150, 113, 20))
        self.lineEdit1.setObjectName("lineEdit1")
        self.lineEdit2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit2.setGeometry(QtCore.QRect(130, 180, 113, 20))
        self.lineEdit2.setObjectName("lineEdit2")
        self.lineEdit3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit3.setGeometry(QtCore.QRect(130, 210, 113, 20))
        self.lineEdit3.setObjectName("lineEdit3")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(130, 270, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox2.setGeometry(QtCore.QRect(130, 310, 69, 22))
        self.comboBox2.setObjectName("comboBox2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 366, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

class StoreCommand(QtWidgets.QUndoCommand):

    def __init__(self, field, text):
        QtWidgets.QUndoCommand.__init__(self)
        # Record the field that has changed.
        self.field = field
        # Record the text at the time the command was created.
        self.text = text

    def undo(self):
        # Remove the text from the file and set it in the field.
        self.field.setText(self.text)

    def redo(self):
        # Store the text in the file and set it in the field.
        self.field.setText(self.text)

class StoreComboCommand(QtWidgets.QUndoCommand):

    def __init__(self, field, text):
        QtWidgets.QUndoCommand.__init__(self)
        # Record the field that has changed.
        self.field = field
        # Record the text at the time the command was created.
        self.text = text

    def undo(self):
        # Remove the text from the file and set it in the field.
        index = self.field.findText(self.text)
        self.field.setCurrentIndex(index)

    def redo(self):
        # Store the text in the file and set it in the field.
        index = self.field.findText(self.text)
        self.field.setCurrentIndex(index)


class Example(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        super().__init__()
        self.setupUi(self)
        self.comboBox.addItem('')
        self.comboBox.addItem('H')
        self.comboBox.addItem('N')
        self.comboBox2.addItem('')
        self.comboBox2.addItem('H')
        self.comboBox2.addItem('N')
        #
        self.undoStack = QtWidgets.QUndoStack()
        self.stackview = QtWidgets.QUndoView(self.undoStack)
        #
        self.lineEdit1.editingFinished.connect(self.storeFieldText)
        self.lineEdit2.editingFinished.connect(self.storeFieldText)
        self.lineEdit3.editingFinished.connect(self.storeFieldText)
        self.comboBox.currentIndexChanged.connect(self.storeFieldComboText)
        self.comboBox2.currentIndexChanged.connect(self.storeFieldComboText)
        #Item actions
        self.undoAction = self.undoStack.createUndoAction(self, self.tr("&Undo"))
        self.undoAction.setShortcuts(QtGui.QKeySequence.Undo)
        self.redoAction = self.undoStack.createRedoAction(self, self.tr("&Redo"))
        self.redoAction.setShortcuts(QtGui.QKeySequence.Redo)

        self.itemToolbar = self.addToolBar("Item actions")
        self.itemToolbar.addAction(self.undoAction)
        self.itemToolbar.addAction(self.redoAction)

    def storeFieldText(self):
        command = StoreCommand(self.sender(),self.sender().text())
        self.undoStack.push(command)

    def storeFieldComboText(self):
        command = StoreComboCommand(self.sender(),self.sender().currentText())
        self.undoStack.push(command)

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = Example()
    gui.show()
    gui.stackview.show()
    sys.exit(app.exec_())    

if __name__ == "__main__":
    main()