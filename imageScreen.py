from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from screen import Screen

from navigation import NavigationController


class ImageScreen(Screen):
    def __init__(self, params: dict, navController: NavigationController):
        super().__init__(params)
        self.navController = navController
        self.imageFile = params.get("IMAGE")
        if self.imageFile == None: raise Exception("no image specified")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(*[0]*4)
        self.imageWidget = self.image()
        self.layout.addWidget(self.imageWidget)
        self.layout.addLayout(self.buttons())
        self.setLayout(self.layout)
        

    def start(self):
        self.loadImage(self.imageWidget, self.imageFile)

    def image(self) -> QWidget:
        imageWidget = QLabel()
        return imageWidget
    
    def loadImage(self, imageWidget, imageFile):
        image = QPixmap(imageFile.filepath)
        image = image.scaled(imageWidget.width(), imageWidget.height(), aspectRatioMode=Qt.KeepAspectRatio)
        self.imageWidget.setPixmap(image)

    def buttons(self) -> QLayout:
        layout = QHBoxLayout()
        returnButton = QPushButton("Return")
        returnButton.clicked.connect(lambda: self.navController.popBackStack())

        layout.addWidget(returnButton)

        return layout