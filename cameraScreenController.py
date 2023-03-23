from controller import Controller
from navigation import NavigationController
from picamera2 import Picamera2
from camera import Camera
from PyQt5.QtCore import QThreadPool

class CameraScreenController(Controller):
    def __init__(self, navController: NavigationController, dispatcher: QThreadPool, camera: Camera):
        self.dispatcher = dispatcher
        self.camera = camera
        self.navController = navController

    def capture(self):
        self.camera.capture()

    def record(self, state: bool, callback=None):
        self.camera.record(state=state, callback=callback)

    def settings(self):
        self.navController.navigate("SETTINGS_SCREEN")

    def gallery(self):
        self.navController.navigate("GALLERY_SCREEN")

    def autofocus(self):
        return self.camera.autofocus()