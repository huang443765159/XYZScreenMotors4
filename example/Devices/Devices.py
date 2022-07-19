from XYZMotors3.Utils.Singleton import singleton

from XYZScreenMotors4.ScreenMotors import ScreenMotors


@singleton
class Devices:

    def __init__(self):
        self.motors = ScreenMotors()

    def exit(self):
        self.motors.exit()
