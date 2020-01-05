import sys
import os
import random
from functools import partial
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from modules import widgetStyleSheet
import icons_rc

# QModelView using QAbstractItemModel - tree model view

class Node(object):
    def __init__(self,name,parent=None):
        self._name = name
        self._children = list()
        self._parent = parent

        #print('\ninit: {}'.format(name))

        if parent is not None:
            parent.addChild(self)

    def typeInfo(self):
        return 'NODE'

    def addChild(self,child):
        #print('Add child: {}'.format(child))
        self._children.append(child)

    def name(self):
        #print('Get name: {}'.format(self._name))
        return self._name

    def setName(self,name):
        self._name = name

    def child(self,row):
        #print('Child row: {}'.format(row))
        return self._children[row]

    def childCount(self):
        #print('Get childCount: {}'.format(len(self._children)))
        return len(self._children)

    def parent(self):
        #print('Get parent: {}'.format(self._parent))
        return self._parent

    def row(self):
        if self._parent is not None:
            #print('Get row: {}'.format(self._parent._children.index(self)))
            return self._parent._children.index(self)
        else:
            pass
            #print('Get row: -1')

    def log(self,tabLevel = -1):
        output = ''
        tabLevel += 1

        for _ in range(tabLevel):
            output += '\t'

        output += self._name + '\n'

        for child in self._children:
            output += child.log(tabLevel)

        tabLevel -= 1

        return output

    def __repr__(self):
        return self.log()

class TransformNode(Node):
    def __init__(self,name,parent):
        super(TransformNode,self).__init__(name,parent)

    def typeInfo(self):
        return 'TRANSFORM'

class CameraNode(Node):
    def __init__(self,name,parent):
        super(CameraNode,self).__init__(name,parent)

    def typeInfo(self):
        return 'CAMERA'

class LightNode(Node):
    def __init__(self,name,parent):
        super(LightNode,self).__init__(name,parent)

    def typeInfo(self):
        return 'LIGHT'

class SceneGraphModel(QtCore.QAbstractItemModel):

    """INPUTS: Node, QObject"""
    def __init__(self,root,parent=None):
        super(SceneGraphModel,self).__init__(parent)
        self._rootNode = root

    """ INPUTS: QModelIndex. OUTPUT: int"""
    def rowCount(self,parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    """ INPUTS: QModelIndex. OUTPUT: int"""
    def columnCount(self,parent):
        return 2
    
    """INPUTS: QModelIndex, int. OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self,index,role):
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.name()
            else:
                return node.typeInfo()

        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                typeInfo = node.typeInfo()

                # the icon images are imported via a compiled icons_rc.py file
                # compile syntax: pyrcc5.exe inputfile.qrc -o outputfile_rc.py
                if typeInfo == 'LIGHT':
                    return QtGui.QIcon(QtGui.QPixmap(":/Light.png"))

                if typeInfo == 'TRANSFORM':
                    return QtGui.QIcon(QtGui.QPixmap(":/Transform.png"))

                if typeInfo == 'CAMERA':
                    return QtGui.QIcon(QtGui.QPixmap(":/Camera.png"))

    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self,index,value,role=QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                node = index.internalPointer()
                node.setName(value)

                return True
        
        return False
    
    """INPUT: int, Qt.Orientation, int. OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self,section,orientation,role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return 'SceneGraph'
            else:
                return 'TypeInfo'

    """INPUT: QModelIndex. OUTPUT: int(flag)"""
    def flags(self,index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    """INPUT: QModelIndex. OUTPUT: QModelIndex, should return the parent of the node with given QModelIndex"""
    def parent(self, index):
        # index refers to the QModelIndex of the current node
        node = self.getNode(index)
        parentNode = node.parent() # from the node class method, find its parent node
        
        if parentNode == self._rootNode:
            # this will happen only when it is at the root node, beginning
            return QtCore.QModelIndex() # return an empty QModelIndex as a mean to say this is the root index
        
        # The goal is to create and return a ModelIndex that is pointing to the parent node
        return self.createIndex(parentNode.row(), 0, parentNode)

    """CUSTOM. INPUTS:QModelIndex"""
    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer() # the internalPointer method will return the current node (node class)
            if node:
                return node
        # If index is not valid meaning the incoming is an empty QModelIndex, root level is detexted
        return self._rootNode
    
    """INPUTS: int, int, QModelIndex. OUTPUT: QModelIndex, should return the QModelIndex that corresponds
       to the given row, column and parent node"""
    def index(self,row,column,parent):
        # parent refers to the QModelIndex type
        parentNode = self.getNode(parent)

        # From the parent node and the given row number we use the child method in the node class
        # to retrieve the child node (node class)
        childItem = parentNode.child(row)

        if childItem:
            # The goal is to create and return a ModelIndex that is pointing to the child node
            return self.createIndex(row,column,childItem)
        else:
            # Unlikely event when child item is invlaid, we return empty QModelIndex
            return QtCore.QModelIndex()



class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        rootNode   = Node("Hips")
        childNode0 = TransformNode("RightPirateLeg",        rootNode)
        childNode1 = Node("RightPirateLeg_END",    childNode0)
        childNode2 = CameraNode("LeftFemur",             rootNode)
        childNode3 = Node("LeftTibia",             childNode2)
        childNode4 = Node("LeftFoot",              childNode3)
        childNode5 = LightNode("LeftFoot_END",          childNode4)
        print(rootNode)

        treeModel = SceneGraphModel(rootNode)

        # ------------ QListWidget ----------------------------
        leftListView = QtWidgets.QListView()

        # ------------ QTreeView ------------------------------
        treeView = QtWidgets.QTreeView()
        treeView.setModel(treeModel)

        # ------------ QPushButton ----------------------------
        debugPushButton = QtWidgets.QPushButton('Debug')
        selectionPushButton = QtWidgets.QPushButton('Selection')
        addPushButton = QtWidgets.QPushButton('Add Row')
        removePushButton = QtWidgets.QPushButton('Remove Row')

        # ------------ Controllers Layout ---------------------
        controllerLayout = QtWidgets.QHBoxLayout()
        controllerLayout.setAlignment(QtCore.Qt.AlignLeft)
        controllerLayout.setSpacing(0)
        controllerLayout.addWidget(debugPushButton)
        controllerLayout.addWidget(selectionPushButton)
        controllerLayout.addWidget(addPushButton)
        controllerLayout.addWidget(removePushButton)

        # ------------ Left Layout ----------------------------
        #leftLayout = QtWidgets.QVBoxLayout()

        # ------------ Right Layout ---------------------------
        rightLayout = QtWidgets.QVBoxLayout()
        rightLayout.addWidget(treeView)
        rightLayout.addLayout(controllerLayout)

        # ------------ mainLayout -----------------------------
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(rightLayout)        

        # ------------ Connections ----------------------------
        #debugPushButton.clicked.connect(partial(self.debug,tableModel))
        #selectionPushButton.clicked.connect(partial(self.getSelection,tableView))
        #addPushButton.clicked.connect(partial(self.addNewRow,tableModel,tableView))
        #removePushButton.clicked.connect(partial(self.removeRow,tableModel,tableView))

        # ------------ mainWidget -----------------------------
        mainWidget = QtWidgets.QWidget()
        mainWidget.setLayout(mainLayout)

        self.setMinimumSize(300, 600)
        self.setWindowTitle("QAbstractItemModel Tree Model View Sample")
        self.setCentralWidget(mainWidget)
        self.show()

    def debug(self):
        pass
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec_())