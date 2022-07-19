from typing import List, Optional, Tuple

from XYZMotors3.Utils.Conf.MotorConf import Conf
from XYZMotors3.OneMotor.RealMotor.RealMotor import RealMotor
from XYZUtil4.config.config_screen_motor import ConfigScreenMotor


class OneMotor:

    def __init__(self, bot_id: int, cid: int):
        self._bot_type = None
        self._cid = cid
        self._conf = Conf(conf_path=ConfigScreenMotor.get_motor_ini_path(bot_id=bot_id, cid=cid))
        self._real = RealMotor(bot_id=bot_id, cid=cid, conf=self._conf, is_screen_motor=True)

    def set_bot_type(self, bot_type: str):
        self._bot_type = bot_type

    def get_bot_type(self) -> Optional[str]:
        return self._bot_type

    def set_link(self, link: bool):
        self._real.set_link(link=link)

    def get_link(self) -> bool:
        return self._real.get_link()

    def get_pos_range(self) -> Tuple[float, float]:
        return self._conf.range0, self._conf.range1

    def get_motor_type(self) -> str:
        return self._conf.motor_type

    def get_spd_max(self) -> float:
        return self._conf.spd_max

    def set_mode(self, mode: bytes):
        self._real.set_mode(mode=mode)

    def set_turbo(self, turbo: float):
        self._real.set_turbo(turbo=turbo)

    def get_turbo(self) -> float:
        return self._real.get_turbo()

    def get_conf(self) -> Conf:
        return self._conf

    # CMD
    def homing(self):
        self._real.homing()

    def org(self):
        self._real.org()

    def move_to_pos(self, pos_tar: float, spd_tar: float = 0.0, safe: bool = True, reply: str = ''):
        self._real.move_to_pos(pos_tar=pos_tar, spd_tar=spd_tar, reply=reply)

    def move_to_spd(self, reply: str = '', reverse: bool = False, spd: float = None):
        self._real.move_to_spd(reply=reply, reverse=reverse, spd=spd)

    def stop(self):
        self._real.stop()

    def load_dance(self, cmd: List[float]):
        self._real.load_dance(cmd=cmd)

    def start_dance(self, reply: str = ''):
        self._real.start_dance(reply=reply)

    def reset(self):
        self._real.reset()

    def get_cur_pos(self) -> float:
        return self._real.get_cur_pos()

    def exit(self):
        if self.get_link():
            self.stop()
