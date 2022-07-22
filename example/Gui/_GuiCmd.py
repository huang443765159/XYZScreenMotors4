from typing import Optional

from XYZMotors4.Utils.Codec import CODEC

from example.Devices.Devices import Devices
from example.Gui.UI.UI import Ui_MainWindow
from XYZScreenMotors4.OneMotor.OneMotor import OneMotor


# TODO：舵机转一段时间后，会突然出现一次转过角度再转回来


class GuiCmd:

    def __init__(self, ui: Ui_MainWindow):
        self._devices = Devices()
        self._motors = self._devices.models
        self._ui = ui
        self._btn_cid = {1: self._ui.cid_1}
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
        self._ui.btn_cid_reset.clicked.connect(self._reset)
        self._ui.btn_brush_once.clicked.connect(self._brush_once)
        self._ui.btn_tv_out.clicked.connect(self._devices.models.tv_out)
        self._ui.btn_tv_in.clicked.connect(self._devices.models.tv_in)
        for cid in self._motors.get_cid_list():
            self._motors.get_one_motor(cid=cid).set_mode(CODEC.MODE.POS)
        self.sign = self._motors.sign
        self.sign.current_error.connect(self._signal_current_error)

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
            one_motor.move_to_spd(reply='MOTOR_BTN', is_add=reverse)

    def _move_to_pos(self):
        one_motor = self._get_motor_cur()
        if one_motor is not None:
            pos_tar = self._ui.pos_tar.value()
            one_motor.move_to_pos(pos_tar=pos_tar)

    def _stop_all(self):
        self._motors.stop()
        self._thread_switch = False

    def _brush_once(self):
        self._motors.wiper.brush_once()

    def _reset(self):
        one_motor = self._get_motor_cur()
        if one_motor is not None:
            one_motor.reset()
