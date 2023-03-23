from PIL import Image, ImageDraw
from collections import deque
from enum import Enum
import numpy

class Position(Enum):
    CENTER = 1
    TOPLEFT = 1

class OverlayImage:

    def __init__(self, image: Image.Image, origin:tuple[int,int]=(0,0)):
        self.origin = origin
        self.image = image

    @classmethod
    def open(cls, path: str, origin:tuple[int,int]=(0,0)):
        image = Image.open(path)
        return cls(image=image, origin=origin)

    def render(self):
        pass

    def pasteOn(self, image: Image.Image):
        self.render()
        image.paste(self.image, box=self.origin)

    def getDraw(self):
        return ImageDraw.Draw(self.image)

    def resize(self, size: tuple[int,int]):
        self.image = self.image.resize(size)

    def scale(self, scale: float):
        self.resize(size=(int(self.image.width * scale), int(self.image.height * scale)))

    def scaleToImage(self, scaleImage: Image.Image, scale: float):
        heightScale = scaleImage.height // self.image.height
        widthScale = scaleImage.width // self.image.width
        if heightScale < widthScale:
            self.scale(heightScale*scale)
        else:
            self.scale(widthScale*scale)

    def toArray(self) -> numpy.array:
        return numpy.array(self.image)

    def clearOverlay(self):
        self.image = Image.new(size=self.image.size, mode="RGBA")

class Overlay(OverlayImage):

    def __init__(self, size: tuple[int,int]=(640,480), image: Image.Image=None, origin:tuple[int,int]=(0,0)):
        self.origin = origin
        self.images = deque()
        self.border = None
        
        if image == None:
            newImage = Image.new(size=size, mode="RGBA") 
        else:
            newImage = image
        super().__init__(image=newImage, origin=origin)

    def setBorder(self, width: int, color: tuple[int,int,int,int]=(0,0,0,255)):
        if self.border != None:
            self.removeImage(self.border)
            self.border = None
        if width == 0:
            self.render()
            return
        borderImage = OverlayImage(image=Image.new(size=self.image.size, mode="RGBA"), origin=(0,0))
        draw = borderImage.getDraw()
        draw.rectangle([0, 0, self.image.size[0]-1, self.image.size[1]-1], outline=color, width=width)
        self.border = borderImage
        self.images.appendleft(borderImage)
        self.render()

    #get image at origin and scale to float of overlay size or image
    def getImage(self, imagePath: str, position: Position=None, origin: tuple[int,int]=(0,0), scale: float=1.0, scaleOverlay: float=None) -> OverlayImage:
        pic = OverlayImage.open(imagePath, origin)
        self.position(pic, position)
        pic.scale(scale)
        if scaleOverlay != None:  
            pic.scaleToImage(self.image, scaleOverlay)
        return pic

    def getCircle(self, size: int, color: tuple[int,int,int,int], position: Position=None, origin: tuple[int,int]=(0,0),) -> OverlayImage:
        circle = OverlayImage(image=Image.new(size=self.image.size, mode="RGBA"), origin=origin)
        self.position(circle, position)
        circle.getDraw().ellipse([0, 0, size, size], fill=color)
        return circle

    def position(self, image: OverlayImage, position: Position):
        overlaySize = self.image.size
        imageSize = image.image.size
        if position == Position.CENTER:
            image.origin = ((overlaySize[0] - imageSize[0]) // 2, (overlaySize[1] - imageSize[1]) // 2)
        elif position == Position.TOPLEFT:
            image.orgin = (0, 0)

    def addImage(self, image, position: Position=None, render=False):
        self.position(image, position)
        self.images.append(image)
        if render: self.render()

    def removeImage(self, image, render=False):
        self.images.remove(image)
        if render:
            self.render()

    def render(self) -> Image.Image:
        self.clearOverlay()
        for image in self.images:
            image.pasteOn(self.image)
        return self.image