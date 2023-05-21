import os
from settings import Settings
from util import pathCheck

class FileService:

    def __init__(self, settings: Settings):
        self.settings = settings

        self.__setImagePath("imagePath", settings.get("imagePath"))
        settings.subscribe("imagePath", self.__setImagePath)

        self.__setVideoPath("videoPath", settings.get("videoPath"))
        settings.subscribe("videoPath", self.__setVideoPath)
       

    def __setImagePath(self, key: str, imagePath: str):
        self.imagePath = os.path.expanduser(imagePath)
        pathCheck(self.imagePath)

    def __setVideoPath(self, key:str, videoPath: str):
        self.videoPath = os.path.expanduser(videoPath)
        pathCheck(self.videoPath)

    def imageDirContents(self):
        contents = os.listdir(self.imagePath)
        contents = filter(self.checkExtension, contents)
        contents = list(map(self.getDescriptor, contents))
        contents.sort(reverse=True)
        return contents

    def checkExtension(self, file):
        extension = os.path.splitext(file)[1].lower()
        if(extension == ".jpg"): return True
        if(extension == ".jpeg"): return True
        return False

    def getImageDescriptor(self, file: str):
        try:
            filePath = os.path.join(self.videoPath, file)
            created = os.path.getmtime(filePath)
            return FileDescriptor(filePath, created)
        except Exception as e:
            print("unable to read file info")

class FileDescriptor:

    def __init__(self, filepath: str, modified: float):
        self.filepath = filepath
        self.modified = modified

    def __lt__(self, other):
        return self.modified < other.modified 

    def __str__(self):
        return self.filepath
    
    def __repr__(self):
        return self.__str__()