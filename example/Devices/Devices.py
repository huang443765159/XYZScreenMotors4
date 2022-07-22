from XYZUtil4.tools.for_class import singleton

from XYZScreenMotors4.ScreenMotors import ScreenMotors


@singleton
class Devices:

    def __init__(self):
        self.models = ScreenMotors()

    def exit(self):
        self.models.exit()
