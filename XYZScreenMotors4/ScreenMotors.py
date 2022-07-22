import struct
from typing import Dict, List, Optional

from XYZUtil4.network.UDP import UDP
from XYZUtil4.config.config_screen_motor import ConfigScreenMotor
from XYZUtil4.config import config_screen_motor

from XYZMotors4.Utils.Signals import Signals
from XYZMotors4.Utils.Conf.BotConf import Conf

from XYZScreenMotors4.OneMotor.OneMotor import OneMotor
from XYZScreenMotors4.OneMotor.OneWiper import OneWiper

WIPER_ADDR = ('192.168.50.80', 54188)


class ScreenMotors:

    def __init__(self, bot_id: int = 1):
        self.bot_type = "Screen"
        self._bot_id = bot_id
        self.sign = Signals()
        self._config = config_screen_motor
        self._cid_list = self._config.get_cid_list(bot_id=bot_id)
        self._motors = {cid: OneMotor(bot_id=bot_id, cid=cid, sign=self.sign) for cid in
                        self._cid_list}  # type: Dict[int, OneMotor]
        self.wiper = OneWiper(wiper_id=1, mcu_addr=WIPER_ADDR)
        self._conf = Conf(conf_path=ConfigScreenMotor().get_bot_ini_path(bot_id=bot_id))
        # NETWORK
        self._udp = UDP(is_nuc=True)
        self._udp.sign_recv.connect(self._udp_recv)
        self.sign.current_error.connect(self._signal_current_error)

    def _udp_recv(self, data: bytes, ip: str, port: int):
        pass

    # SIGNALS
    def _signal_current_error(self, bot_type: str, bot_id: int, cid: int, data: bytes):
        print('ERROR', bot_type, bot_id, cid, data)

    # API
    def _get_first_motor(self) -> Optional[OneMotor]:
        first_motor = None
        if self._motors:
            first_motor = list(self._motors.values())[0]
        return first_motor

    def get_one_motor(self, cid: int) -> Optional[OneMotor]:
        return self._motors.get(cid)

    def get_bot_id(self) -> int:
        return self._bot_id

    def get_cid_list(self) -> List[int]:
        return self._cid_list

    def set_link(self, link: bool):
        for motor in self._motors.values():
            motor.set_link(link=link)

    def get_link(self) -> bool:
        link = False
        if self._motors:
            link = self._get_first_motor().get_link()
        return link

    def set_turbo(self, turbo: float):
        for motor in self._motors.values():
            motor.set_turbo(turbo=turbo)

    def get_turbo(self) -> float:
        turbo = None
        if self._motors:
            turbo = self._get_first_motor().get_turbo()
        return turbo

    def stop(self):
        for motor in self._motors.values():
            motor.stop()

    def exit(self):
        for motor in self._motors.values():
            motor.exit()
