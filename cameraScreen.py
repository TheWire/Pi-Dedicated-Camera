from PyQt5.QtWidgets import QLayout, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QThread
from screen import Screen
from util import Runnable
from cameraPreview import CameraPreview
from cameraScreenController import CameraScreenController
from gpioService import GPIOService, GPIODevice

class CameraScreen(Screen):

    BORDER_SIZE = 2

    def __init__(self, params: dict, width: int, height: int, gpioService: GPIOService, controller: CameraScreenController):
        super().__init__()
        self.controller = controller
        self.gpioService = gpioService

        self.recording = False

        self.gpioSetup()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(*[0]*4)

        self.cameraPreview = self.camera(width, height)
        self.layout.addWidget(self.cameraPreview)
        
        buttonRow = self.buttons(controller)
        self.layout.addLayout(buttonRow)

        self.setLayout(self.layout)

    def gpioSetup(self):
        self.subscriptions = {}
        subscription = self.gpioService.subscribe(GPIODevice.SHUTTER, self.captureImage)
        self.subscriptions[subscription] = GPIODevice.SHUTTER

    def gpioClose(self):
        for subscription, device in self.subscriptions.items():
            self.gpioService.unsubscribe(device, subscription)

    def previewClick(self):
        if self.controller.autofocus():
            self.cameraPreview.setBorder((66, 245, 66, 200),size=10)
        else:
            self.cameraPreview.setBorder((245, 66, 66, 200),size=10)
        QThread.sleep(3)
        self.cameraPreview.setBorder(color=None)

    def camera(self, width, height):
        cameraPreview = CameraPreview(self.controller.camera.camera, width=width, height=height-80)
        cameraPreview.mousePressEvent = lambda event: self.controller.dispatcher.start(Runnable(0, self.previewClick))
        return cameraPreview

    def captureImage(self):
        self.cameraPreview.setCameraIcon(set=True)
        self.controller.capture()
        self.cameraPreview.setCameraIcon(set=False)

    def recordHandler(self):
        def onRecordChange():
            self.enableButtons(state= not self.recording, excluded=self.record)
            text = "Stop" if self.recording else "Record"
            self.record.setText(text)
            self.cameraPreview.setRecordingIcon(set=self.recording)
        self.recording = not self.recording
        self.controller.record(state=self.recording, callback=onRecordChange)

    def enableButtons(self, state: bool=True, excluded: QPushButton=None):
        for button in self.buttonWidgets:
            if excluded is button: continue
            button.setEnabled(state)


    def buttons(self, controller) -> QLayout:
        row = QHBoxLayout()
        row.setContentsMargins(*[4]*4)
        self.buttonWidgets = []
        self.capture = QPushButton("Capture")
        self.capture.clicked.connect(self.captureImage)
        self.buttonWidgets.append(self.capture)
        self.record= QPushButton("Record")
        self.record.clicked.connect(self.recordHandler)
        self.buttonWidgets.append(self.record)
        self.settings = QPushButton("Settings")
        self.settings.clicked.connect(controller.settings)
        self.buttonWidgets.append(self.settings)
        self.gallery = QPushButton("Gallery")
        self.gallery.clicked.connect(controller.gallery)
        self.buttonWidgets.append(self.gallery)
        row.addWidget(self.capture)
        row.addWidget(self.settings)
        row.addWidget(self.gallery)
        row.addWidget(self.record)
        
        return row

    def end(self):
        self.gpioClose()
        self.cameraPreview.cleanup()
