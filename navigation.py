from collections import deque
from controller import Controller
from screen import Screen
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtCore import QTimer

class NavigationPath:
    def __init__(self, widget: type[Screen], widgetArgs: list, controller: type[Controller]=None, controllerArgs: list=None):
        self.widget = widget
        self.widgetArgs = widgetArgs
        self.controllerClass = controller
        self.controllerArgs = controllerArgs
        self.instantiated = False

    def getScreen(self):
        if not self.instantiated: raise Exception("Path not instantiated")
        if self.controller != None:
            return self.widget(self.params, controller=self.controller, *self.widgetArgs)
        else:
            return self.widget(self.params, *self.widgetArgs)

    def instantiate(self, params: dict={}) -> QWidget:
        self.params = params
        self.controller = None
        if self.controllerClass != None:
            self.controller = self.controllerClass(*self.controllerArgs)
        self.instantiated = True
    
class NavigationController:
    def __init__(self, mainWidget: QMainWindow):
        self.mainWidget = mainWidget
        self.paths = {}
        self.navStack = deque()
        self.currentScreen= None

    def setPath(self, path: str, navigationPath: NavigationPath):
        self.paths[path] = navigationPath

    def navigate(self, path: str, params: dict={}):
        navPath = self.paths.get(path)
        if navPath == None:
            raise Exception("invalid path")
        navPath.instantiate(params)
        self.navStack.append(navPath)
        self.__navigate()
        

    def __navigate(self):
        if self.currentScreen is not None: self.currentScreen.end()
        self.currentScreen = self.navStack[-1].getScreen()
        self.mainWidget.setCentralWidget(self.currentScreen)
        QTimer.singleShot(5, self.currentScreen.start)


    def popBackStack(self):
        self.navStack.pop()
        self.__navigate()