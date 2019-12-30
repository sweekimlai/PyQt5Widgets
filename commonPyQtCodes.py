###################### common PyQt codes ######################
import sys
import os
from functools import partial
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets

# ------------ QListWidget ------------------------------------

# add list item to list widget and make it editable
def addItemsToList(self,listWidget,listContents):    
    for i in listContents:
        listItem = QtWidgets.QListWidgetItem(i)
        listItem.setFlags(listItem.flags()|QtCore.Qt.ItemIsEditable)            
        listWidget.addItem(listItem)