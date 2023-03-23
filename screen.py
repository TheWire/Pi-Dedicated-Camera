from PyQt5.QtWidgets import QWidget
from controller import Controller

class Screen(QWidget):
    def __init__(self, params: dict={}, controller: Controller=None):
        super().__init__()
        self.params = params
        self.controller = controller

    #runs after screen added to window
    def start(self):
        pass

    def end(self):
        pass