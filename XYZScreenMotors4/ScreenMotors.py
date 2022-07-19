import struct
from typing import Dict, List, Optional

from XYZUtil4.network.UDP import UDP
from XYZUtil4.config.config_screen_motor import ConfigScreenMotor

from XYZMotors3.Adv.OneBotAdv import OneBotAdv
from XYZMotors3.Utils.Codec import CODEC
from XYZMotors3.Utils.Signals import Signals
from XYZMotors3.Utils.Conf.BotConf import Conf

from XYZScreenMotors4.OneMotor.OneMotor import OneMotor


class ScreenMotors:

    def __init__(self, bot_id: int = 0):
        self._bot_type = None
        self._bot_id = bot_id
        self._cid_list = ConfigScreenMotor().get_cid_list(bot_id=bot_id)
        self._motors = {cid: OneMotor(bot_id=bot_id, cid=cid) for cid in self._cid_list}  # type: Dict[int, OneMotor]
        self._conf = Conf(conf_path=ConfigScreenMotor().get_bot_ini_path(bot_id=bot_id))
        # NETWORK
        self._udp = UDP(is_nuc=True)
        self._udp.sign_recv.connect(self._udp_recv)
        self._motor_dance_ready_cache = dict()
        self._adv = OneBotAdv(one_bot=self)
        self._dance_count = 0
        self.sign = Signals()
        self.sign.current_error.connect(self._signal_current_error)
        self.sign.motor_dance_ready.connect(self._signals_motor_dance_ready)

    def _udp_recv(self, data: bytes, ip: str, port: int):
        pass

    # SIGNALS
    def _signal_current_error(self, bot_type: str, bot_id: int, cid: int, data: bytes):
        print('ERROR', bot_type, bot_id, cid, data)

    def _signals_motor_dance_ready(self, bot_type: str, bot_id: int, cid: int):
        if bot_id == self._bot_id and cid in self._motor_dance_ready_cache:
            self._motor_dance_ready_cache[cid] = False
            if None not in self._motor_dance_ready_cache.values():
                self.sign.bot_dance_ready.emit(bot_type, bot_id)

    # API
    def _get_first_motor(self) -> Optional[OneMotor]:
        first_motor = None
        if self._motors:
            first_motor = list(self._motors.values())[0]
        return first_motor

    def get_one_motor(self, cid: int) -> Optional[OneMotor]:
        return self._motors.get(cid)

    def set_bot_type(self, bot_type: str):
        self._bot_type = bot_type
        for motor in self._motors.values():
            motor.set_bot_type(bot_type=bot_type)

    def get_bot_type(self) -> Optional[str]:
        bot_type = None
        if self._motors:
            bot_type = self._get_first_motor().get_bot_type()
        return bot_type

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

    # ADV
    def load_dance(self, cmd: Dict[int, List[float]]):
        self._motor_dance_ready_cache.clear()
        for cid, motor_cmd in cmd.items():
            self._motor_dance_ready_cache[cid] = None
            one_motor = self._motors[cid]
            one_motor.load_dance(cmd=motor_cmd)

    def start_dance(self, reply: str = ''):
        for motor in self._motors.values():
            motor.start_dance(reply=reply)
        if self.get_link():
            data = CODEC.HEAD.START_DANCE + struct.pack('!B', self._dance_count) + b'\x01\x01\x01\x01\x01\01'
            print(self._cid_list, data)
            self._udp.send_to(data=data, ip=self._conf.reset_board_ip, port=self._conf.reset_board_port)
            self._dance_count += 1
            if self._dance_count >= 256:
                self._dance_count = 0

    def go_to(self, pos_queue: list, reply: str = ''):
        self._adv.go_to(pos_queue=pos_queue, reply=reply)

    def go_safe(self, pos_x: float, reply: str = ''):
        self._adv.go_safe(pos_x=pos_x, reply=reply)

    def exit(self):
        for motor in self._motors.values():
            motor.exit()
