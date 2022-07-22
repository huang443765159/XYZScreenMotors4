from configparser import ConfigParser
from datetime import datetime
from pathlib import PosixPath


class Conf:

    def __init__(self, conf_path: PosixPath):
        self._conf = ConfigParser()
        self._conf.read(conf_path)
        self._conf_path = conf_path
        # MCU
        self.mcu_ip = self._conf.get(section='MCU', option='ip')
        self.mcu_port = self._conf.getint(section='MCU', option='port')
        self.math_motor_port = 0
        # PHYSICAL
        self.motor_type = self._conf.get(section='PHYSICAL', option='motor_type')
        ratio_a, ratio_b = self._conf.get(section='PHYSICAL', option='gear_ratio').split(':')
        self.gear_ratio = float(ratio_a) / float(ratio_b)
        self.gear_diameter = self._conf.getfloat(section='PHYSICAL', option='gear_diameter')
        # CALIBRATION
        self.calib_reverse = self._conf.getboolean(section='CALIBRATION', option='calib_reverse')
        self.calib_max_current = self._conf.getfloat(section='CALIBRATION', option='calib_max_current')
        # PID
        self.pos_gain = self._conf.getfloat(section='PID', option='pos_gain')
        self.spd_gain = self._conf.getfloat(section='PID', option='spd_gain')
        self.spd_integrator_gain = self._conf.getfloat(section='PID', option='spd_integrator_gain')
        self.spd_limit = self._conf.getfloat(section='PID', option='spd_limit')
        self.inertia = self._conf.getfloat(section='PID', option='inertia')
        self.current_lim = self._conf.getfloat(section='PID', option='current_lim')
        # MOTION
        self.motion_type = self._conf.get(section='MOTION', option='motion_type')
        self.reverse_dir = self._conf.getboolean(section='MOTION', option='reverse_dir')
        self.acc = self._conf.getfloat(section='MOTION', option='acc')
        self.emergency_stop_dec = self._conf.getfloat(section='MOTION', option='emergency_stop_dec')
        self.spd_max = self._conf.getfloat(section='MOTION', option='spd_max')
        self.range0 = self._conf.getfloat(section='MOTION', option='range0')
        self.range1 = self._conf.getfloat(section='MOTION', option='range1')
        # HOMING
        self.org_pos = self._conf.getfloat(section='HOMING', option='org_pos')
        self.homing_acc = self._conf.getfloat(section='HOMING', option='homing_acc')
        self.homing_spd = self._conf.getfloat(section='HOMING', option='homing_spd')

    def _get_math_motor_port(self) -> int:
        return int(self.mcu_ip.split('.')[-1]) + 54000

    def save_conf(self):
        self._conf.set(section='PID', option='pos_gain', value=str(self.pos_gain))
        self._conf.set(section='PID', option='spd_gain', value=str(self.spd_gain))
        self._conf.set(section='PID', option='spd_integrator_gain', value=str(self.spd_integrator_gain))
        self._conf.set(section='PID', option='spd_limit', value=str(self.spd_limit))
        self._conf.set(section='PID', option='inertia', value=str(self.inertia))
        self._conf.set(section='PID', option='current_lim', value=str(self.current_lim))
        self._conf.set(section='MOTION', option='acc', value=str(self.acc))
        self._conf.set(section='MOTION', option='spd_max', value=str(self.spd_max))
        self._conf.set(section='MOTION', option='range0', value=str(self.range0))
        self._conf.set(section='MOTION', option='range1', value=str(self.range1))
        self._conf.set(section='UPDATE', option='date', value=datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M'))
        with open(self._conf_path, 'w') as ini_fp:
            self._conf.write(fp=ini_fp)

    def is_motor_reverse_dir(self) -> bool:
        return self.reverse_dir
