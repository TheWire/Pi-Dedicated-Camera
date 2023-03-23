from PyQt5.QtWidgets import QLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt

from screen import Screen
from settingsController import SettingsController
class SettingsScreen(Screen):
    def __init__(self, params: dict, controller: SettingsController):
        super().__init__()
        self.controller = controller
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addLayout(self.createButtonRow())
        backButton = QPushButton("Back")
        backButton.clicked.connect(lambda: controller.back())
        self.layout.addWidget(backButton)

    def createButtonRow(self) -> QLayout:
        layout = QHBoxLayout()
        shutdownButton = QPushButton("Shutdown")
        shutdownButton.clicked.connect(self.controller.shutdown)
        layout.addWidget(shutdownButton)
        restartButton = QPushButton("Restart")
        restartButton.clicked.connect(self.controller.restart)
        layout.addWidget(restartButton)
        layout.setAlignment(Qt.AlignTop)
        return layout
