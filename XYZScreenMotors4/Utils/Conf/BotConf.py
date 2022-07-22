from configparser import ConfigParser
from pathlib import PosixPath


class Conf:

    def __init__(self, conf_path: PosixPath):
        self._conf = ConfigParser()
        self._conf.read(conf_path)
        self._conf_path = conf_path
        # RESET_BOARD
        self.reset_board_ip = self._conf.get(section='RESET_BOARD', option='ip')
        self.reset_board_port = self._conf.getint(section='RESET_BOARD', option='port')
