from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QObject, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap

from screen import Screen
from galleryController import GalleryController
from gpioService import GPIOService, GPIODevice

class GalleryEvent(QObject):
    cwEvent = pyqtSignal()
    ccwEvent = pyqtSignal()
    switchEvent = pyqtSignal()

class GalleryScreen(Screen):

    ROW_SIZE = 2
    
    def __init__(self, params: dict, gpioService: GPIOService, controller: GalleryController):
        super().__init__()
        self.controller = controller
        self.gpioService = gpioService
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.imageLayout= self.images()
        controller.getPageContents()
        controller.setPageChangeCallback(self.loadImages)
        self.layout.addWidget(self.imageLayout)
        self.buttonLayout = self.buttons()
        self.layout.addLayout(self.buttonLayout)
        self.gpioSetup()
        self.selected = None
        self.selectedTimeoutSetup()

        

    def selectedTimeoutSetup(self):
        self.selectedTimer= QTimer()
        self.selectedTimer.timeout.connect(self.removeBorder)
        self.selectedTimer.setSingleShot(True)

    def callbackGenerator(self, eventObject):
        def callback():
            eventObject.emit()
        return callback

    def gpioSetup(self):
        self.subscriptions = {}
        self.events = GalleryEvent()

        self.events.cwEvent.connect(self.picUp)
        subscription = self.gpioService.subscribe(GPIODevice.ROTARY_ENCODER_CW, self.callbackGenerator(self.events.cwEvent))
        self.subscriptions[subscription] = GPIODevice.ROTARY_ENCODER_CW
        
        self.events.ccwEvent.connect(self.picDown)
        subscription = self.gpioService.subscribe(GPIODevice.ROTARY_ENCODER_CCW, self.callbackGenerator(self.events.ccwEvent))
        self.subscriptions[subscription] = GPIODevice.ROTARY_ENCODER_CCW

        self.events.switchEvent.connect(self.switchPicture)
        subscription = self.gpioService.subscribe(GPIODevice.ENCODER_SWITCH, self.callbackGenerator(self.events.switchEvent))
        self.subscriptions[subscription] = GPIODevice.ENCODER_SWITCH
        

    def gpioClose(self):
        for subscription, device in self.subscriptions.items():
            self.gpioService.unsubscribe(device, subscription)

    @pyqtSlot()
    def switchPicture(self):
        if self.selected  is None:
            self.setSelected()
            return
        self.controller.toImage(self.controller.imageSelected)
    
    @pyqtSlot()
    def picUp(self):
        if self.selected  is None:
            self.setSelected()
            return
        self.controller.incrementSelected()
        self.setSelected()
        
    @pyqtSlot()
    def picDown(self):
        if self.selected is None:
            self.setSelected()
            return
        self.controller.decrementSelected()
        self.setSelected()

    def removeBorder(self):
            self.selected.setStyleSheet("border: none;")
            self.selected = None

    def setSelected(self):

        if self.selected is not None:
            self.selectedTimer.stop()
            self.removeBorder()

        self.selected = self.images[self.controller.imageSelected]
        self.selected.setStyleSheet("border: 2px solid rgb(66, 245, 66);")
        self.selectedTimer.start(5000)

    def start(self):
        self.loadImages()

    def images(self) -> QWidget:
        imageContainer = QWidget()
        imageContainer.setStyleSheet("QLabel { border: 1px solid black; background-color: black; }")
        grid = QGridLayout()
        grid.setContentsMargins(*[0]*4)
        imageContainer.setLayout(grid)
        self.images = []
        pageSize = self.controller.filesPerPage
        for i in range(0, pageSize):
            imageWidget = QLabel()
            imageWidget.setAlignment(Qt.AlignCenter)

            def imageClicked(idx):
                return lambda event: self.controller.toImage(idx)
            
            imageWidget.mousePressEvent = imageClicked(i)
            self.images.append(imageWidget)
            grid.addWidget(imageWidget,i // self.ROW_SIZE, i % self.ROW_SIZE)
        return imageContainer
    
    def buttons(self):
        layout = QHBoxLayout()
        backButton = QPushButton("Return")
        backButton.clicked.connect(lambda: self.controller.back())
        

        lastPageButton = QPushButton("Back")
        lastPageButton.clicked.connect(lambda: [self.controller.prevPage(), self.loadImages()])
        nextPageButton = QPushButton("Forward")
        nextPageButton.clicked.connect(lambda: [self.controller.nextPage(), self.loadImages()])

        layout.addWidget(lastPageButton)
        layout.addWidget(backButton)
        layout.addWidget(nextPageButton)

        return layout
    
    def loadImages(self):
        i = 0
        for imageWidget in self.images:
            if i < len(self.controller.pageContents):
                pic = QPixmap(self.controller.pageContents[i].filepath)
                pic = pic.scaled(imageWidget.width(), imageWidget.height(), aspectRatioMode=Qt.KeepAspectRatio)
                imageWidget.setPixmap(pic)
                imageWidget.show()
            else:
                imageWidget.hide()
            i+=1


    def end(self):
        self.controller.setPageChangeCallback(None)
        self.gpioClose()