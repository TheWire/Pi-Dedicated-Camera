from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2
from overlay import Overlay, Position

class CameraPreview(QGlPicamera2):
    def __init__(self, camera: Picamera2, width: int, height: int):
        super().__init__(camera, width=width, height=height, keep_ar=True)
        self.overlay = Overlay(size=(1920, 1080))
        self.cameraIcon = self.overlay.getImage(imagePath="./image/camera.png", position=Position.CENTER, scaleOverlay=0.25)
        self.recordingIcon = self.overlay.getCircle(size=80, color=(235, 64, 52, 200), origin=(20, 20))
        self.setOverlay()
    
    def setBorder(self, color: tuple[int, int, int, int]=None, size: int=1):
        if size == 0 or color == None:
            self.overlay.setBorder(width=0)
        self.overlay.setBorder(width=size, color=color)
        self.setOverlay()

    def setCameraIcon(self, set: bool=True):
        if set:
            self.overlay.addImage(self.cameraIcon)
        else:
            self.overlay.removeImage(self.cameraIcon)
        self.overlay.render()
        self.setOverlay()

    def setRecordingIcon(self, set: bool=True):
        if set:
            self.overlay.addImage(self.recordingIcon)
        else:
            self.overlay.removeImage(self.recordingIcon)
        self.overlay.render()
        self.setOverlay()

    def setOverlay(self):
        self.set_overlay(self.overlay.toArray())