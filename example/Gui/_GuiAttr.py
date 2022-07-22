from PyQt5.QtGui import QColor
from PyQt5.QtCore import QObject, pyqtSignal

from XYZUtil4.config.config_screen_motor import ConfigScreenMotor

from XYZMotors4.Utils.Codec import CODEC
from XYZMotors4.Utils.Const import CONST

from example.Utils import QTools
from example.Devices.Devices import Devices
from example.Gui.UI.UI import Ui_MainWindow


# TODO：舵机Dance不走，moveto报错，明天调试


class ROW:
    POS_RANGE = 0
    SPD_MAX = 1
    MODE = 2
    POS_CUR = 3
    RPM_CUR = 4
    CUR_CUR = 5
    VOL_CUR = 6
    ODOMETER = 7
    ERROR = 8
    TEMP_ENV = 9
    HUMI_ENV = 10
    TEMP_MOT = 11
    IP = 12
    TYPE = 13


class GuiAttr(QObject):
    # sign_pos_spd = pyqtSignal()
    sign_mode = pyqtSignal(str, int, int, bytes)  # bot_type, bot_id, cid, mode
    sign_pos_spd = pyqtSignal(str, str, int, int, float, float, float)  # source, bot_type, bot_id, cid, ts, pos, spd
    sign_voltage_current = pyqtSignal(str, int, int, float, float)  # bot_type, bot_id, cid, voltage, current
    # bot_type, bot_id, cid, temperature_environment, humidity_environment, temperature_motor
    sign_temperature_humidity = pyqtSignal(str, int, int, float, float, float)

    def __init__(self, ui: Ui_MainWindow):
        super().__init__()
        self._devices = Devices()
        self._motors = self._devices.models
        self._sign = self._motors.sign
        self._ui = ui
        QTools.table_init(table=self._ui.table_motors, select_as_columns=True, no_edit=True)
        # SIGNALS
        self.sign_mode.connect(self._signal_mode)
        self.sign_pos_spd.connect(self._signal_pos_spd)
        self.sign_temperature_humidity.connect(self._signal_temp_humi)
        self.sign_voltage_current.connect(self._signal_voltage_current)

        self._sign.mode.connect(self.sign_mode.emit)
        self._sign.pos_spd.connect(self.sign_pos_spd.emit)
        self._sign.voltage_current.connect(self.sign_voltage_current.emit)
        self._sign.temperature_humidity.connect(self.sign_temperature_humidity.emit)
        self._update()

    def _update(self):
        bot_id = self._devices.models._bot_id
        cid_list = ConfigScreenMotor().get_cid_list(bot_id=bot_id)
        for col in range(self._ui.table_motors.columnCount()):
            cid = col + 1
            if cid in cid_list:
                for row in range(self._ui.table_motors.rowCount()):
                    item = self._ui.table_motors.item(row, col)
                    item.setForeground(QColor(255, 255, 255))
                    item.setText('')
                motor = self._motors.get_one_motor(cid=cid)
                # POS_RANGE
                range0, range1 = motor.get_pos_range()
                if motor.get_motor_type() in [CONST.TYPE.S_TURN, CONST.TYPE.M_TURN]:
                    pos_range = f'{range0:.0f} - {range1:.0f}'
                else:
                    pos_range = f'{range0:.3f} - {range1:.3f}'
                self._ui.table_motors.item(ROW.POS_RANGE, col).setText(pos_range)
                # SPD_MAX
                self._ui.table_motors.item(ROW.SPD_MAX, col).setText(f'{motor.get_spd_max():.4f}')
                # IP
                conf = motor.get_conf()
                self._ui.table_motors.item(ROW.IP, col).setText(conf.mcu_ip)
                self._ui.table_motors.item(ROW.TYPE, col).setText(conf.motor_type)
            else:
                for row in range(self._ui.table_motors.rowCount()):
                    item = self._ui.table_motors.item(row, col)
                    item.setText('x')
                    item.setForeground(QColor(60, 60, 60))

    def _signal_pos_spd(self, source: str, bot_type: str, bot_id: int, cid: int, ts: float, pos: float, spd: float):
        col = cid - 1
        self._ui.table_motors.item(ROW.POS_CUR, col).setText(f'{pos:.3f}')
        self._ui.table_motors.item(ROW.RPM_CUR, col).setText(f'{spd:.3f}')

    def _signal_mode(self, bot_type: str, bot_id: int, cid: int, mode: bytes):
        col = cid - 1
        mode_str = 'OFF'
        if mode == CODEC.MODE.POS:
            mode_str = 'POS'
        elif mode == CODEC.MODE.SPD:
            mode_str = 'SPD'
        self._ui.table_motors.item(ROW.MODE, col).setText(mode_str)

    def _signal_voltage_current(self, bot_tyoe: str, bot_id: int, cid: int, voltage: float, current: float):
        col = cid - 1
        self._ui.table_motors.item(ROW.CUR_CUR, col).setText(f'{current:.1f}')
        self._ui.table_motors.item(ROW.VOL_CUR, col).setText(f'{voltage:.1f}')

    def _signal_temp_humi(self,
                          bot_type: str,
                          bot_id: int,
                          cid: int,
                          temperature_environment: float,
                          humidity_environment: float,
                          temperature_motor: float):
        col = cid - 1
        self._ui.table_motors.item(ROW.TEMP_ENV, col).setText(f'{temperature_environment:.1f}')
        self._ui.table_motors.item(ROW.HUMI_ENV, col).setText(f'{humidity_environment:.1f}')
        self._ui.table_motors.item(ROW.TEMP_MOT, col).setText(f'{temperature_motor:.1f}')
