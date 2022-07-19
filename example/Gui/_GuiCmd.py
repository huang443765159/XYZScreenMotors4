import time
import threading
from typing import Optional

from XYZMotors3.Utils.Codec import CODEC

from example.Devices.Devices import Devices
from example.Gui.UI.UI import Ui_MainWindow
from XYZScreenMotors4.OneMotor.OneMotor import OneMotor
from XYZScreenMotors4.Utils.GetDanceCmd import get_pos_list

# TODO：舵机转一段时间后，会突然出现一次转过角度再转回来


class GuiCmd:

    def __init__(self, ui: Ui_MainWindow):
        self._devices = Devices()
        self._motors = self._devices.motors
        self._ui = ui
        self._btn_cid = {1: self._ui.cid_1, 2: self._ui.cid_2, 3: self._ui.cid_3}
        # BUTTON
        self._ui.btn_mode_pos.clicked.connect(lambda: self._set_mode(mode=CODEC.MODE.POS))
        self._ui.btn_mode_spd.clicked.connect(lambda: self._set_mode(mode=CODEC.MODE.SPD))
        self._ui.btn_mode_off.clicked.connect(lambda: self._set_mode(mode=CODEC.MODE.OFF))
        self._ui.motors_link.clicked.connect(self._set_link)
        self._ui.btn_cid_homing.clicked.connect(self._homing)
        self._ui.btn_cid_org.clicked.connect(self._org)
        self._ui.btn_cid_move_to.clicked.connect(self._move_to_pos)
        self._ui.btn_motor_left.pressed.connect(lambda: self._move_to_spd(reverse=True))
        self._ui.btn_motor_right.pressed.connect(lambda: self._move_to_spd(reverse=False))
        self._ui.btn_motor_left.released.connect(self._stop_all)
        self._ui.btn_motor_right.released.connect(self._stop_all)
        self._ui.btn_motors_stop_all.clicked.connect(self._stop_all)
        self._ui.btn_load_dance.clicked.connect(self._load_dance)
        self._ui.btn_start_dance.clicked.connect(self._start_dance)
        self._ui.btn_start_dance_all.clicked.connect(self._load_dance_all)
        self._ui.btn_cid_reset.clicked.connect(self._reset)
        for cid in range(1, 3):
            self._motors.get_one_motor(cid=cid).set_mode(CODEC.MODE.POS)
        self.sign = self._motors.sign
        self.sign.current_error.connect(self._signal_current_error)
        # TEST_THREAD
        self._thread = None  # type: Optional[threading.Thread]
        self._thread_switch = False

    def _signal_current_error(self, bot_type: str, bot_id: int, cid: int, data: bytes):
        print('ERROR', bot_type, bot_id, cid, data)
        self._stop_all()

    def _get_motor_cur(self) -> Optional[OneMotor]:
        cid = 0
        for cid, btn_cid in self._btn_cid.items():
            if btn_cid.isChecked():
                break
        one_motor = self._motors.get_one_motor(cid=cid)
        return one_motor

    def _set_link(self, link: bool):
        self._motors.set_link(link=link)

    def _set_mode(self, mode: bytes):
        one_motor = self._get_motor_cur()
        if one_motor is not None:
            one_motor.set_mode(mode=mode)

    def _homing(self):
        one_motor = self._get_motor_cur()
        if one_motor is not None:
            one_motor.homing()

    def _org(self):
        one_motor = self._get_motor_cur()
        if one_motor is not None:
            one_motor.org()

    def _move_to_spd(self, reverse: bool):
        one_motor = self._get_motor_cur()
        if one_motor is not None:
            one_motor.move_to_spd(reply='MOTOR_BTN', reverse=reverse)

    def _move_to_pos(self):
        one_motor = self._get_motor_cur()
        if one_motor is not None:
            pos_tar = self._ui.pos_tar.value()
            one_motor.move_to_pos(pos_tar=pos_tar, safe=self._ui.motors_safe.isChecked())

    def _stop_all(self):
        self._motors.stop()
        self._thread_switch = False

    def _load_dance(self):
        one_motor = self._get_motor_cur()
        if one_motor is not None:
            spd = self._ui.dance_spd.value()
            acc = self._ui.dance_spd.value()
            pos_s = self._ui.dance_pos_s.value()
            pos_e = self._ui.dance_pos_e.value()
            max_jerk = 3 if one_motor.get_conf().motor_type == 'FOC' else 200
            pos_list = get_pos_list(max_vel=spd, max_acc=acc, max_jerk=max_jerk, pos_start=pos_s, pos_end=pos_e)
            one_motor.load_dance(cmd=pos_list)

    def _start_dance(self):
        # self._thread = threading.Thread(target=self._working, daemon=True)
        # self._thread_switch = True
        # self._thread.start()
        self._motors.start_dance()

    def _working(self):
        while self._thread_switch:
            self._load_dance_all()
            self._motors.start_dance()
            time.sleep(7)

    def _load_dance_all(self):   # 电机1和2为镜像关系，1号电机正走，2号电机负走
        # spd = self._ui.dance_spd.value()
        # acc = self._ui.dance_spd.value()
        # pos_s = self._ui.dance_pos_s.value()
        # pos_e = self._ui.dance_pos_e.value()
        # for cid in [2, 3]:
        #     pos_list = get_pos_list(max_vel=spd, max_acc=acc, max_jerk=3, pos_start=pos_s if cid == 3 else -pos_s,
        #                             pos_end=pos_e if cid == 3 else -pos_e)
        #     self._motors.get_one_motor(cid=cid).load_dance(cmd=pos_list)
        # for cid in [2, 3]:
        #     spd, acc = 0.25, 0.25
        #     pos_s = self._motors.get_one_motor(cid=cid).get_cur_pos()
        #     pos_e = (-0.5 if cid == 3 else 0.5) if -0.01 < pos_s < 0.01 else 0
        #     pos_list = get_pos_list(max_vel=spd, max_acc=acc, max_jerk=3, pos_start=pos_s, pos_end=pos_e)
        #     self._motors.get_one_motor(cid=cid).load_dance(cmd=pos_list)
        spd, acc = 200, 200
        pos_s = self._motors.get_one_motor(cid=1).get_cur_pos()
        if -1 < pos_s < 1 or 359 < pos_s < 360:
            pos_s = 0
            pos_e = 180
        else:
            pos_s = 180
            pos_e = 0
        pos_list = get_pos_list(max_vel=spd, max_acc=acc, max_jerk=200, pos_start=pos_s, pos_end=pos_e)
        self._motors.get_one_motor(cid=1).load_dance(cmd=pos_list)

    def _reset(self):
        one_motor = self._get_motor_cur()
        if one_motor is not None:
            one_motor.reset()
