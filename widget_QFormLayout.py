import sys
import os
from functools import partial
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from modules import widgetStyleSheet

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        # ------------ QLabel ---------------------------------
        nameLabel = QtWidgets.QLabel('Name:')
        addressLabel = QtWidgets.QLabel('Address:')
        emptyLabel = QtWidgets.QLabel('')

        # ------------ QDialogButtonBox -----------------------
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        # ------------ QLineEdit ------------------------------
        nameLineEdit = QtWidgets.QLineEdit()
        addressALineEdit = QtWidgets.QLineEdit()
        addressBLineEdit = QtWidgets.QLineEdit()
        addressCLineEdit = QtWidgets.QLineEdit()

        nameLineEdit.setPlaceholderText('Enter name here')
        addressALineEdit.setPlaceholderText('Enter address here')

        addressALineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        
        # ------------ QVBoxLayout ----------------------------
        addressLayout = QtWidgets.QVBoxLayout()
        addressLayout.addWidget(addressALineEdit)
        addressLayout.addWidget(addressBLineEdit)
        addressLayout.addWidget(addressCLineEdit)
        addressLayout.setSpacing(5)

        # ------------ FormLayout -----------------------------
        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow(nameLabel,nameLineEdit)
        formLayout.addRow(addressLabel,addressLayout)
        formLayout.addRow(emptyLabel,buttonBox)
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
        

    def accept(self):
        print('You Accepted')

    def reject(self):
        print('You Rejected')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec_())