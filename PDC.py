from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThreadPool
from picamera2 import Picamera2

from navigation import NavigationController, NavigationPath
from cameraScreen import CameraScreen
from cameraScreenController import CameraScreenController
from settingsScreen import SettingsScreen
from settingsController import SettingsController
from galleryScreen import GalleryScreen
from galleryController import GalleryController
from imageScreen import ImageScreen
from camera import Camera
from fileService import FileService
from gpioService import GPIOService
from settings import Settings

import os
os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

    
class PiCamera:
    def __init__(self):

        self.gpioService = GPIOService()
        self.app = QApplication([])
        self.threadPool = QThreadPool.globalInstance()
        self.win = QMainWindow()
        self.win.setWindowTitle("Pi Dedicated Camera")
        self.size = self.app.primaryScreen().size()
        self.win.resize(480, 320)
        self.win.setFixedSize(480, 320)
        self.settings = Settings()
        self.settings.read()
        self.camera = Camera(Picamera2(), settings=self.settings)
        fileService = FileService("~/Pictures/pi_dslr")
        self.navController = NavigationController(self.win)
        cameraScreenControllerArgs = [self.navController, self.threadPool, self.camera]
        cameraScreen = NavigationPath(widget = CameraScreen, widgetArgs=[self.size.height(), self.size.width(), self.gpioService], controller=CameraScreenController, controllerArgs=cameraScreenControllerArgs)
        self.navController.setPath("CAMERA_SCREEN", cameraScreen)

        settingsScreen = NavigationPath(widget = SettingsScreen, widgetArgs=[], controller=SettingsController, controllerArgs =[self.navController, self.settings])
        self.navController.setPath("SETTINGS_SCREEN", settingsScreen)

        galleryScreen = NavigationPath(widget = GalleryScreen, widgetArgs=[self.gpioService], controller=GalleryController, controllerArgs = [self.navController, fileService])
        self.navController.setPath("GALLERY_SCREEN", galleryScreen)

        imageScreen = NavigationPath(widget = ImageScreen, widgetArgs=[self.navController])
        self.navController.setPath("IMAGE_SCREEN", imageScreen)
    
    def start(self):
        self.navController.navigate("CAMERA_SCREEN")
        self.camera.start()
        # self.win.showFullScreen()
        self.win.show()
        self.app.exec()

piCamera = PiCamera()
piCamera.start()