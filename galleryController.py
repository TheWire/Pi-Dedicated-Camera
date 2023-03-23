from controller import Controller
from navigation import NavigationController
from fileService import FileService
import math

class GalleryController(Controller):

    def __init__(self, navController: NavigationController, fileService: FileService):
        self.navController = navController
        self.fileService = fileService
        self.imageFiles = []
        self.pageContents = []
        self.filesPerPage = 4
        self.page = 0
        self.imageSelected = 0
        self.onPageChange = None

    def incrementSelected(self):
        self.imageSelected += 1
        if self.imageSelected >= len(self.pageContents):
            self.nextPage()

    def decrementSelected(self):
        self.imageSelected -= 1
        if self.imageSelected < 0:
            self.prevPage()

    def back(self):
        self.navController.popBackStack()

    def getPageContents(self):
        if len(self.imageFiles) == 0:
            self.imageFiles = self.fileService.dirContents()
            self.numPages = int(math.ceil(len(self.imageFiles) / self.filesPerPage))
        imageStart = self.page * self.filesPerPage
        self.pageContents = self.imageFiles[imageStart:imageStart + self.filesPerPage]

    def setPageChangeCallback(self, callback):
        self.onPageChange = callback

    def nextPage(self):
        self.imageSelected = 0
        self.page += 1
        if self.page == self.numPages:
            self.page = 0
        self.getPageContents()
        if self.onPageChange is not None:
            self.onPageChange()

    def prevPage(self):
        self.page -= 1
        if self.page < 0:
            self.page = self.numPages - 1      
        self.getPageContents()
        self.imageSelected = len(self.pageContents) - 1
        if self.onPageChange is not None:
            self.onPageChange()

    def toImage(self, imagePageIdx: int):
        self.navController.navigate("IMAGE_SCREEN",params={"IMAGE": self.pageContents[imagePageIdx]})