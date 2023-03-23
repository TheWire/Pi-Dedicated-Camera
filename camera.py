import libcamera
from os import path
from libcamera import controls
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from time import time
from settings import Settings
from  util import pathCheck

class Camera:
    def __init__(self, camera: Picamera2, settings: Settings):
        self.camera = camera
        try:
            self.camera.set_controls({"AfMode": controls.AfModeEnum.Manual})
            self.autofocusEnabled = True
        except:
            self.autofocusEnabled = False
        self.settings = settings
        self.stillConfig = camera.create_video_configuration(
            main={"size": (4608, 2592)},
            lores={"size": (384, 216)},
            transform=libcamera.Transform(),
            colour_space=libcamera.ColorSpace.Sycc(),
            buffer_count=4,
            display="lores",
            encode="main",
            queue=True
        )
        self.videoConfig = camera.create_video_configuration(
            main={"size": (1920, 1080)},
            lores={"size": (480, 270)},
            transform=libcamera.Transform(),
            colour_space=libcamera.ColorSpace.Sycc(),
            buffer_count=4,
            display="lores",
            encode="main",
            queue=True
        )
        self.camera.configure(self.stillConfig)

        self.__setImagePath("imagePath", settings.get("imagePath"))
        settings.subscribe("imagePath", self.__setImagePath)

        self.__setVideoPath("videoPath", settings.get("videoPath"))
        settings.subscribe("videoPath", self.__setVideoPath)

    def __setImagePath(self, key: str, imagePath: str):
        self.imagePath = path.expanduser(imagePath)

    def __setVideoPath(self, key:str, videoPath: str):
        self.videoPath = path.expanduser(videoPath)

    def start(self):
        self.camera.start()

    #True for continuous False for Manual
    def switchAutofocusMode(self, state: bool=False) -> bool:
        if not self.autofocusEnabled: return False
        if state: self.camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        else: self.camera.set_controls({"AfMode": controls.AfModeEnum.Manual})
        return True

    def autofocus(self) -> bool:
        if not self.autofocusEnabled: return False
        return self.camera.autofocus_cycle(wait=True)

    def capture(self):
        pathCheck(self.imagePath)
        filePath = path.join(self.imagePath, str(int(time())) + ".jpg")
        i = 0
        while path.exists(filePath):
            i += 1
            filePath = path.join(self.imagePath, str(int(time())) + f"_{i}.jpg")
        self.camera.capture_file(filePath)


    def __record(self, callback=None):
        def startRecord(job):
            self.camera.wait(job)
            self.switchAutofocusMode(state=True)
            videoPath = path.join(self.videoPath, str(int(time())) + ".mp4")
            encoder = H264Encoder(10000000)
            encoder.output = FfmpegOutput(videoPath)
            self.camera.start_encoder(encoder)
            if callback is not None: callback()
        return startRecord

    def __stopRecord(self, callback):
        def stop(job):
            self.camera.wait(job)
            self.switchAutofocusMode(state=False)
            if callback is not None: callback()
        return stop
    
    def record(self, state=True, callback=None):
        if state:
            pathCheck(self.videoPath)
            self.camera.switch_mode(self.videoConfig, signal_function=self.__record(callback))
        else:
            self.camera.stop_encoder()
            self.camera.switch_mode(self.stillConfig, signal_function=self.__stopRecord(callback))