from gpiozero import Button, RotaryEncoder, DigitalOutputDevice
from enum import Enum

class GPIODevice(Enum):
    ROTARY_ENCODER=1
    ROTARY_ENCODER_CW=2
    ROTARY_ENCODER_CCW=3
    ENCODER_SWITCH=4
    SHUTTER=5


class GPIOService:
    def __init__(self):
        self.__setupShutterButton(19)
        self.__setupRotaryEncoder(cwPin=13, ccwPin=6, switchPin=5, powerPin=12)


    def __setupShutterButton(self, pin: int):
        self.shutter = Button(pin)
        self.shutterSubscribers = {}
        self.shutter.when_pressed = self.__handler_generator(self.shutterSubscribers)

    def __setupRotaryEncoder(self, cwPin: int, ccwPin: int, switchPin: int, powerPin: int=None):
        if powerPin != None:
            self.power = DigitalOutputDevice(powerPin)
            self.power.on()
        self.rotor = RotaryEncoder(cwPin, ccwPin)
        self.rotorSubscribers = {}
        self.cwSubscribers = {}
        self.ccwSubscribers = {}
        self.rotor.when_rotated = self.__handler_generator(self.rotorSubscribers)
        
        self.rotor.when_rotated_clockwise = self.__handler_generator(self.cwSubscribers)
        self.rotor.when_rotated_counter_clockwise = self.__handler_generator(self.ccwSubscribers)
        
        self.switch = Button(switchPin)
        self.switchSubscribers = {}
        self.switch.when_pressed = self.__handler_generator(self.switchSubscribers)

    def __handler_generator(self, subscribers):
        def handle():
            for callback in subscribers.values():
                callback()
        return handle


    def subscribe(self, device: GPIODevice, callback) -> int:
        subRef = id(callback)
        if device == GPIODevice.ROTARY_ENCODER:
            self.rotorSubscribers[subRef] = callback
        elif device == GPIODevice.ROTARY_ENCODER_CW:
            self.cwSubscribers[subRef] = callback
        elif device == GPIODevice.ROTARY_ENCODER_CCW:
            self.ccwSubscribers[subRef] = callback
        elif device == GPIODevice.ENCODER_SWITCH:
            self.switchSubscribers[subRef] = callback
        elif device == GPIODevice.SHUTTER:
            self.shutterSubscribers[subRef] = callback
        return subRef

    def unsubscribe(self, device: GPIODevice, subRef: int):
        if device == GPIODevice.ROTARY_ENCODER:
            del self.rotorSubscribers[subRef]
        elif device == GPIODevice.ROTARY_ENCODER_CW:
            del self.cwSubscribers[subRef]
        elif device == GPIODevice.ROTARY_ENCODER_CCW:
            del self.ccwSubscribers[subRef]
        elif device == GPIODevice.ENCODER_SWITCH:
            del self.switchSubscribers[subRef]
        elif device == GPIODevice.SHUTTER:
            del self.shutterSubscribers[subRef]
