from math import sqrt, fabs, pow
from numpy import arange, diff

STEP_TIME = 0.01
# 减速比 1：32， 齿轮直径6cm


class _TrajTime:
    def __init__(self, vel_time: float, acc_time: float, jerk_time: float):
        self.jerk_time = jerk_time
        self.acc_time = acc_time
        self.vel_time = vel_time

    def get_sum_time(self) -> float:
        sum_time = self.jerk_time * 4 + self.acc_time * 2 + self.vel_time
        return sum_time


class _TrajParam:
    def __init__(self, max_vel: float, max_acc: float, max_jerk: float, pos_start: float, pos_end: float):
        self.max_jerk = fabs(max_jerk)
        self.max_acc = fabs(max_acc)
        self.max_vel = fabs(max_vel)
        self.point_start = pos_start
        self.point_end = pos_end

    def set_vel(self, set_vel: float):
        self.max_vel = set_vel

    def set_acc(self, set_acc: float):
        self.max_acc = set_acc

    def set_jerk(self, set_jerk: float):
        self.max_jerk = set_jerk


def _build_param(traj_param: _TrajParam, time_step: float, min_distance: float) -> _TrajTime:
    distance = traj_param.point_end - traj_param.point_start
    traj_dir = 1 if distance > 0 else -1
    distance = fabs(distance)
    traj_time = _TrajTime(jerk_time=-1, acc_time=-1, vel_time=-1)
    if distance < min_distance:
        return traj_time
    # STAGE_1_MAKE_SURE_T_J
    t_jerk = traj_param.max_acc / traj_param.max_jerk
    if distance < 2 * traj_param.max_jerk * t_jerk ** 3:
        traj_time.jerk_time = pow(distance * 0.5 / traj_param.max_jerk, 1 / 3)
        traj_time.acc_time = 0
        traj_time.vel_time = 0
        traj_param.set_jerk(traj_param.max_jerk * traj_dir)
        traj_param.set_acc(traj_param.max_acc * traj_dir)
        traj_param.set_vel(traj_param.max_vel * traj_dir)
        return traj_time
    if traj_param.max_vel < traj_param.max_jerk * pow(t_jerk, 2):
        traj_time.jerk_time = sqrt(traj_param.max_vel / traj_param.max_jerk)
        traj_time.acc_time = 0
        traj_time.vel_time = (distance - 2.0 * traj_param.max_jerk * pow(t_jerk, 3.0)) / traj_param.max_vel
        traj_param.set_jerk(traj_param.max_jerk * traj_dir)
        traj_param.set_acc(traj_param.max_acc * traj_dir)
        traj_param.set_vel(traj_param.max_vel * traj_dir)
        return traj_time
    traj_time.jerk_time = t_jerk
    # STAGE_2_MAKE_SURE_T_A
    t_acc = (traj_param.max_vel - traj_param.max_jerk * pow(t_jerk, 2)) / traj_param.max_acc
    if distance < traj_param.max_jerk * t_jerk * t_acc ** 2 + 3.0 * traj_param.max_jerk * t_jerk ** 2 * t_acc + 2.0 * traj_param.max_jerk * t_jerk ** 3:
        traj_time.jerk_time = t_jerk
        traj_time.acc_time = -1.5 * t_jerk + sqrt(pow(t_jerk, 2) / 4.0 + distance / (traj_param.max_jerk * t_jerk))
        traj_time.vel_time = 0
        traj_param.set_jerk(traj_param.max_jerk * traj_dir)
        traj_param.set_acc(traj_param.max_acc * traj_dir)
        traj_param.set_vel(traj_param.max_vel * traj_dir)
        return traj_time
    # STAGE_3_MAKE_SURE_T_V
    t_vel = distance / (traj_param.max_jerk * t_jerk * (t_jerk + t_acc)) - (
            pow(t_acc, 2) + 3.0 * t_jerk * t_acc + 2.0 * pow(t_jerk, 2)) / (t_jerk + t_acc)
    traj_time.jerk_time = t_jerk
    traj_time.acc_time = t_acc
    traj_time.vel_time = t_vel
    traj_param.set_jerk(traj_param.max_jerk * traj_dir)
    traj_param.set_acc(traj_param.max_acc * traj_dir)
    traj_param.set_vel(traj_param.max_vel * traj_dir)
    return traj_time


def _calculate_pos(traj_time: _TrajTime, traj_param: _TrajParam, time_now: float) -> float:
    if traj_time.jerk_time == -1:
        return traj_param.point_end
    pos = traj_param.point_start
    jerk = traj_param.max_jerk
    if time_now >= 0 and time_now < traj_time.jerk_time:
        pos += 1.0 / 6.0 * pow(time_now, 3) * jerk
        print(f"{time_now} : 1 is {pos}")
    elif time_now >= traj_time.jerk_time and time_now < traj_time.jerk_time + traj_time.acc_time:
        acc = jerk * traj_time.jerk_time
        vel = 0.5 * jerk * pow(traj_time.jerk_time, 2)
        pos += 1.0 / 6.0 * pow(traj_time.jerk_time, 3) * jerk + 0.5 * acc * pow(time_now - traj_time.jerk_time,
                                                                                2) + vel * (
                       time_now - traj_time.jerk_time)
        print(f"{time_now} : 2 is {pos}")
    elif time_now >= traj_time.jerk_time + traj_time.acc_time and time_now < 2.0 * traj_time.jerk_time + traj_time.acc_time:
        acc = jerk * traj_time.jerk_time
        vel = jerk * traj_time.jerk_time * (traj_time.acc_time + traj_time.jerk_time * 0.5)
        pos += 1.0 / 6.0 * jerk * pow(traj_time.jerk_time,
                                      3) + 0.5 * jerk * traj_time.acc_time * traj_time.jerk_time * (
                       traj_time.acc_time + traj_time.jerk_time) + 1.0 / 6.0 * (-jerk) * pow(
            time_now - traj_time.acc_time - traj_time.jerk_time, 3) + 0.5 * acc * pow(
            time_now - traj_time.acc_time - traj_time.jerk_time, 2) + vel * (
                       time_now - traj_time.acc_time - traj_time.jerk_time)
        print(f"{time_now} : 3 is {pos}")
    elif time_now >= 2.0 * traj_time.jerk_time + traj_time.acc_time and time_now < 2.0 * traj_time.jerk_time + traj_time.acc_time + traj_time.vel_time:
        vel = jerk * traj_time.jerk_time * (traj_time.acc_time + traj_time.jerk_time)
        pos += jerk * traj_time.jerk_time * traj_time.acc_time * (
                0.5 * traj_time.acc_time + 1.5 * traj_time.jerk_time) + \
               jerk * pow(traj_time.jerk_time, 3) + vel * (time_now - traj_time.acc_time - traj_time.jerk_time * 2.0)
        print(f"{time_now} : 4 is {pos}")
    elif time_now >= 2.0 * traj_time.jerk_time + traj_time.acc_time + traj_time.vel_time and time_now < 3.0 * traj_time.jerk_time + traj_time.acc_time + traj_time.vel_time:
        vel = jerk * traj_time.jerk_time * (traj_time.acc_time + traj_time.jerk_time)
        pos += jerk * traj_time.jerk_time * (
                traj_time.acc_time + traj_time.jerk_time) * traj_time.vel_time + jerk * traj_time.jerk_time * traj_time.acc_time * (
                       traj_time.acc_time * 0.5 + traj_time.jerk_time * 1.5) + jerk * pow(traj_time.jerk_time, 3) \
               + 1.0 / 6.0 * (-jerk) * pow(
            (time_now - traj_time.jerk_time * 2.0 - traj_time.acc_time - traj_time.vel_time), 3) + vel * (
                       time_now - traj_time.jerk_time * 2.0 - traj_time.acc_time - traj_time.vel_time)
        print(f"{time_now} : 5 is {pos}")
    elif time_now >= 3.0 * traj_time.jerk_time + traj_time.acc_time + traj_time.vel_time and time_now < 3.0 * traj_time.jerk_time + 2.0 * traj_time.acc_time + traj_time.vel_time:
        acc = -jerk * traj_time.jerk_time
        vel = jerk * traj_time.jerk_time * (traj_time.acc_time + traj_time.jerk_time) - 0.5 * jerk * pow(
            traj_time.jerk_time, 2)
        pos += (jerk * traj_time.jerk_time * traj_time.acc_time + jerk * pow(traj_time.jerk_time,
                                                                             2)) * traj_time.vel_time + jerk * traj_time.jerk_time * pow(
            traj_time.acc_time, 2) * 0.5 + 2.5 * jerk * pow(traj_time.jerk_time,
                                                            2) * traj_time.acc_time + 11.0 / 6.0 * jerk * pow(
            traj_time.jerk_time, 3) + 0.5 * acc * pow(
            time_now - traj_time.jerk_time * 3.0 - traj_time.acc_time - traj_time.vel_time, 2) + vel * (
                       time_now - traj_time.jerk_time * 3 - traj_time.acc_time - traj_time.vel_time)
        print(f"{time_now} : 6 is {pos}")

    elif time_now >= 3.0 * traj_time.jerk_time + 2.0 * traj_time.acc_time + traj_time.vel_time and time_now < 4.0 * traj_time.jerk_time + 2.0 * traj_time.acc_time + traj_time.vel_time:
        acc = -jerk * traj_time.jerk_time
        vel = jerk * traj_time.jerk_time * (traj_time.acc_time + traj_time.jerk_time) + 0.5 * (-jerk) * pow(
            traj_time.jerk_time,
            2) + acc * traj_time.acc_time
        pos += jerk * traj_time.jerk_time * (
                traj_time.acc_time + traj_time.jerk_time) * traj_time.vel_time + jerk * traj_time.jerk_time * traj_time.acc_time * (
                       traj_time.acc_time + traj_time.jerk_time * 3) + 11.0 / 6.0 * jerk * pow(traj_time.jerk_time,
                                                                                               3) + \
               1.0 / 6.0 * jerk * pow(
            time_now - 3.0 * traj_time.jerk_time - 2.0 * traj_time.acc_time - traj_time.vel_time,
            3) + 0.5 * acc * pow(
            time_now - 3.0 * traj_time.jerk_time - 2.0 * traj_time.acc_time - traj_time.vel_time, 2) + vel * (
                       time_now - 3.0 * traj_time.jerk_time - 2.0 * traj_time.acc_time - traj_time.vel_time)

        print(f"{time_now} : 7 is {pos}")
    elif time_now >= 4.0 * traj_time.jerk_time + 2.0 * traj_time.acc_time + traj_time.vel_time:
        pos = traj_param.point_end
        print(f"{time_now} : 8 is {pos}")
    return pos


def get_pos_list(max_vel: float, max_acc: float, max_jerk: int, pos_start: float, pos_end: float) -> list:
    traj_param = _TrajParam(max_vel=max_vel, max_acc=max_acc, max_jerk=max_jerk, pos_start=pos_start, pos_end=pos_end)
    traj_time = _build_param(traj_param=traj_param, time_step=STEP_TIME, min_distance=0.01)
    time_sum = traj_time.get_sum_time() + STEP_TIME
    pos_list, time_list = list(), list()
    for time_now in arange(0, time_sum, STEP_TIME):
        pos_list.append(_calculate_pos(traj_param=traj_param, traj_time=traj_time, time_now=time_now))
        time_list.append(time_now)
    return pos_list


# if __name__ == "__main__":
#     import math
#     from matplotlib import pyplot
#
#     traj_param = _TrajParam(max_vel=0.3, max_acc=0.3, max_jerk=3, pos_start=0, pos_end=0.5)  # 最大速度，最大加速度，加加，
#     traj_time = _build_param(traj_param=traj_param, time_step=STEP_TIME, min_distance=0.01)
#     time_sum = traj_time.get_sum_time() + STEP_TIME
#     pos_list, time_list = list(), list()
#     for time_now in arange(0, time_sum, STEP_TIME):
#         pos_list.append(_calculate_pos(traj_param=traj_param, traj_time=traj_time, time_now=time_now))
#         time_list.append(time_now)
#     # rpm_list = [one_pos / (math.pi * 6 / 1000) * 32 * 10000 for one_pos in pos_list]
#     # print(rpm_list)
#     vel_list = diff(pos_list) / STEP_TIME
#     acc_list = diff(vel_list) / STEP_TIME
#     pyplot.subplot(3, 1, 1)
#     pyplot.plot(time_list, pos_list, label='pos')
#     pyplot.legend(loc=1)
#     pyplot.subplot(3, 1, 2)
#     pyplot.plot(time_list[:-1], vel_list, label='vel')
#     pyplot.legend(loc=1)
#     pyplot.subplot(3, 1, 3)
#     pyplot.plot(time_list[1:-1], acc_list, label='acc')
#     pyplot.legend(loc=1)
#     pyplot.show()
