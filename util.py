from PyQt5.QtCore import QRunnable
from os import path, mkdir

class Runnable(QRunnable):
    def __init__(self, n, task):
        super().__init__()
        self.n = n
        self.task = task

    def run(self):
        self.task()


def pathCheck(dirPath: str):
        print(dirPath)
        if not path.exists(dirPath):
            mkdir(dirPath)