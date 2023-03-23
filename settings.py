import json
import os
from util import pathCheck

class Settings:

    SETTINGS_TEMPLATE = {
        "imagePath": [str],
        "videoPath": [str]
    }

    DEFAULT_SETTINGS = {
        "imagePath": "~/Pictures/pi_dslr",
        "videoPath": "~/Videos/pi_dslr"
    }

    def __init__(self, settingsPath: str="config/"):
        routePath = os.path.expanduser(settingsPath)
        pathCheck(routePath)
        self.settingsPath = os.path.join(routePath, "settings.json")
        self.__settings = self.DEFAULT_SETTINGS
        self.__subscriptions = {}

    def parse(self, settings: dict)-> dict:
        parsedSettings = {}
        for setting, value in settings.items():
            template = self.SETTINGS_TEMPLATE.get(settings)
            if  template is None or type(value) not in template: continue
            parsedSettings[setting] = value
        return parsedSettings
    
    def mergeDefaultValues(self, settings: dict) -> dict:
        return self.DEFAULT_SETTINGS | settings

    def subscribe(self, key: str, callback) -> int:
        if key not in self.__settings: return -1
        if self.__subscriptions.get(key) is None: self.__subscriptions[key] = {}
        subscription = id(callback)
        self.__subscriptions[key][subscription] = callback
        return subscription

    def unsubscribe(self, key: str, subscription: int) -> int:
        callbacks = self.__subscriptions.get(key)
        if callbacks is None: return
        callbacks.remove(subscription)

    def set(self, key: str, value) -> bool:
        if key not in self.SETTINGS_TEMPLATE: return False
        if type(value) is not self.SETTINGS_TEMPLATE[key]: return False
        self.__settings[key] = value
        callbacks = self.__subscriptions.get(key)
        if callbacks == None: return
        for callback in callbacks.values():
            callback(key, value)
        self.write()

    def get(self, key: str, default=None):
        return self.__settings.get(key, default)

    def read(self):
        try:
            f = open(self.settingsPath)
            settings = json.load(f)
            settings = self.parseSettings(settings)
            settings = self.mergeDefaultValues(settings)
            print(settings)
            self.__settings = settings
            f.close()
        except:
            self.__settings = self.DEFAULT_SETTINGS
            self.write()

    def write(self):
        try:
            f = open(self.settingsPath, "w")
            json.dump(self.__settings, f)
            f.close()
        except Exception as e:
            print(f"{e} error writing settings")