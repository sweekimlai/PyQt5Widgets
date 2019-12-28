import sys
from functools import partial
from PyQt5 import QtCore
from PyQt5 import QtWidgets

class TabBarCustom(QtWidgets.QTabBar):    
    addTabClicked = QtCore.pyqtSignal()

    def __init__(self,parent):
        super(TabBarCustom,self).__init__()
        self.setParent(parent)

        self.setTabsClosable(True)

        self.setStyleSheet(
        """
            QTabBar::tab {
                width: 120px;
            }

           QTabBar::tab:selected {
                color: rgb(0,0,0,255);
                background: rgb(75,167,222,255);
           }

           QTabBar::tab:!selected{
                color: rgb(255,255,255,255);
                background: rgb(175,175,175,255);
            }

        """)

    def contextMenuEvent(self,event):
        menu = QtWidgets.QMenu(self)
        addTabAction = menu.addAction('Add tab')
        renameTabAction = menu.addAction('Rename tab')
        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == renameTabAction:
            self.renameTab()
        elif action == addTabAction:
            self.addTab()

    def renameTab(self):
        self.setTabText(self.currentIndex(),'Renamed Tab')

    def addTab(self):
        self.addTabClicked.emit()

class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__()

        # ------------ Menu Bar -------------------------------
        mainMenuBar = self.menuBar()
        tabMenu = mainMenuBar.addMenu('Tabs')
        addTabAction = QtWidgets.QAction('Add New Tab',self)
        
        tabMenu.addAction(addTabAction)

        # ------------ QPushButton ----------------------------
        buttonA = QtWidgets.QPushButton('Button A: How many tabs')
        buttonB = QtWidgets.QPushButton('Button B')

        # ------------ tabALayout -----------------------------
        tabALayout = QtWidgets.QVBoxLayout()
        tabALayout.addWidget(buttonA)

        # ------------ tabBLayout -----------------------------
        tabBLayout = QtWidgets.QVBoxLayout()
        tabBLayout.addWidget(buttonB)

        # ------------ QTabWidget -----------------------------
        mainTabs = QtWidgets.QTabWidget()
        mainTabs.setTabShape(mainTabs.Rounded)
        mainTabs.setMovable(True)

        customTabBar = TabBarCustom(self)
        mainTabs.setTabBar(customTabBar)
                
        tabA = QtWidgets.QWidget()
        tabB = QtWidgets.QWidget()

        tabA.setLayout(tabALayout)
        tabB.setLayout(tabBLayout)

        mainTabs.addTab(tabA, 'Tab A')
        mainTabs.addTab(tabB, 'Tab B')

        self.setFirstTabNotClosable(mainTabs)

        # ------------ Connections ----------------------------
        buttonA.clicked.connect(partial(self.countTabNum, mainTabs))
        mainTabs.tabCloseRequested.connect(partial(self.closeTab, mainTabs))
        addTabAction.triggered.connect(partial(self.addNewTab, mainTabs))
        customTabBar.addTabClicked.connect(partial(self.addNewTab, mainTabs))
        
        self.setMinimumSize(600, 500)
        self.setWindowTitle("QTabWidget Sample")
        self.setCentralWidget(mainTabs)
        self.show()

    def setFirstTabNotClosable(self,tabWidget):
        tabWidget.tabBar().setTabButton(0,QtWidgets.QTabBar.RightSide,None)

    def countTabNum(self,tabWidget):
        print('There are {} tabs'.format(tabWidget.count()))

    def closeTab(self,tabWidget,index):
        if tabWidget.count() > 1:
            tabWidget.removeTab(index)

    def addNewTab(self,tabWidget):        
        newPushButton = QtWidgets.QPushButton('New Button')
        newTabLayout = QtWidgets.QVBoxLayout()
        newTabLayout.addWidget(newPushButton)

        newTab = QtWidgets.QWidget()
        newTab.setLayout(newTabLayout)

        newPushButton.clicked.connect(partial(self.countTabNum, tabWidget))

        tabWidget.addTab(newTab, 'new tab')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec_())