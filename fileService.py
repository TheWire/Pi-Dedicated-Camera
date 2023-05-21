import os
from util import pathCheck

class FileService:

    def __init__(self, dirPath: str):
        self.dirPath = os.path.expanduser(dirPath)

    def dirContents(self):
        pathCheck(self.dirPath)
        contents = os.listdir(self.dirPath)
        contents = filter(self.checkExtension, contents)
        contents = list(map(self.getDescriptor, contents))
        contents.sort(reverse=True)
        return contents

    def checkExtension(self, file):
        extension = os.path.splitext(file)[1].lower()
        if(extension == ".jpg"): return True
        if(extension == ".jpeg"): return True
        return False

    def getDescriptor(self, file: str):
        try:
            filePath = os.path.join(self.dirPath, file)
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