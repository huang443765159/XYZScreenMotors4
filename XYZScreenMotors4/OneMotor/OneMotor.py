import multiprocessing
import time
from typing import List, Tuple

from XYZMotors4.OneMotor.MathMotor.MathMotor import MathMotor
from XYZMotors4.OneMotor.RealMotor.RealMotor import RealMotor
from XYZMotors4.Utils.Conf.MotorConf import Conf
from XYZMotors4.Utils.Signals import Signals
from XYZUtil4.config.config_screen_motor import ConfigScreenMotor


class OneMotor:

    def __init__(self, bot_id: int, cid: int, sign: Signals):
        self._bot_id = bot_id
        self._cid = cid
        self._conf = Conf(conf_path=ConfigScreenMotor.get_motor_ini_path(bot_id=bot_id, cid=cid))
        self._real = RealMotor(bot_id=bot_id, cid=cid, conf=self._conf, sign=sign)
        while True:
            ip, port = self._real.get_udp_addr()
            if port != 0:
                break
            time.sleep(0.02)
        self._process_event = multiprocessing.Event()
        self._process = multiprocessing.Process(target=self._working,
                                                args=(bot_id, cid, self._conf, port, self._process_event))
        self._process.start()

    def get_bot_id(self) -> int:
        return self._bot_id

    def get_cid(self) -> int:
        return self._cid

    def get_error_msg(self) -> str:
        return self._real.get_error_msg()

    def set_link(self, link: bool):
        self._real.set_link(link=link)

    def get_link(self) -> bool:
        return self._real.get_link()

    def get_pos_range(self) -> Tuple[float, float]:
        return self._conf.range0, self._conf.range1

    def get_motor_type(self) -> str:
        return self._conf.motor_type

    def get_motion_type(self) -> str:
        return self._conf.motion_type

    def get_spd_max(self) -> float:
        return self._conf.spd_max

    def get_acc_max(self) -> float:
        return self._conf.acc

    def set_mode(self, mode: bytes):
        self._real.set_mode(mode=mode)

    def get_mode(self) -> bytes:
        return self._real.get_mode()

    def set_safe(self, safe: bool):
        self._real.set_safe(safe=safe)

    def get_safe(self) -> bool:
        return self.get_safe()

    def set_turbo(self, turbo: float):
        self._real.set_turbo(turbo=turbo)

    def get_turbo(self) -> float:
        return self._real.get_turbo()

    def get_conf(self) -> Conf:
        return self._conf

    def get_pos_cur(self) -> float:
        return self._real.get_pos_cur()

    def get_spd_rpm_cur(self) -> float:
        return self._real.get_spd_rpm_cur()

    # CMD
    def homing(self):
        if self.get_link():
            self._real.homing()

    def org(self):
        self._real.org()

    def move_to_pos(self, pos_tar: float, spd_tar: float = 0.0, reply: str = ''):
        self._real.move_to_pos(pos_tar=pos_tar, spd_tar=spd_tar, reply=reply)

    def move_to_spd(self, reply: str = '', is_add: bool = False, spd: float = None):
        self._real.move_to_spd(reply=reply, is_add=is_add, spd=spd)

    def stop(self):
        self._real.stop()

    def go_dance(self, cmd: List[float], reply: str = ''):
        self._real.go_dance(cmd=cmd, reply=reply)

    def start_dance(self):
        self._real.start_dance()

    def reset(self):
        self._real.reset()

    @staticmethod
    def _working(bot_id: int, cid: int, conf: Conf, real_motor_port: int, process_event: multiprocessing.Event):
        # while True:
        #     ip, port = self._real.get_udp_addr()
        #     if port != 0:
        #         break
        #     time.sleep(0.02)
        math_motor = MathMotor(bot_id=bot_id, cid=cid, conf=conf, real_motor_port=real_motor_port)
        process_event.wait()
        math_motor.exit()

    def exit(self):
        self._process_event.set()
        self._process.kill()
        if self.get_link():
            self.stop()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._process.kill()
