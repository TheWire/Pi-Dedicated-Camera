import os
from controller import Controller
from navigation import NavigationController
from settings import Settings

class SettingsController(Controller):

    def __init__(self, navController: NavigationController, settings: Settings):
        self.navController = navController

    def back(self):
        self.navController.popBackStack()

    def shutdown(self):
        os.system("sudo shutdown now")

    def restart(self):
        os.system("sudo shutdown -r now")