from XYZUtil4.customclass.Signal import Signal


class Signals:
    # SIGN_NETWORK
    foc_online = Signal(str, int, int, bool)  # bot_type, bot_id, cid, is_online
    error = Signal(str, int, int, str)  # bot_type, bot_id, cid, error_msg
    # SIGN_ATTR
    mode = Signal(str, int, int, bytes)  # bot_type, bot_id, cid, mode
    pos_spd = Signal(str, str, int, int, float, float, float)  # source, bot_type, bot_id, cid, ts, pos, spd_rpm
    reached = Signal(str, str, int, int, float, float, str)  # source, bot_type, bot_id, cid, ts, pos, reply
    # SIGN_MOVING
    motor_dance_ready = Signal(str, int, int)  # bot_type, bot_id, cid
    bot_dance_ready = Signal(str, int)  # bot_type, bot_id
    # MOTOR_STATUS
    voltage_current = Signal(str, int, int, float, float)  # bot_type, bot_id, cid, voltage, current
    # bot_type, bot_id, cid, temperature_environment, humidity_environment, temperature_motor
    temperature_humidity = Signal(str, int, int, float, float, float)
    # ADV
    go_to_finished = Signal(str, str, int, dict, str)  # source, bot_type, bot_id, pos_dict, reply
    go_to_all_finished = Signal(str, str, dict, str)  # source, bot_type, pos_dict, reply
    go_safe_finished = Signal(str, str, int, float, str)  # source, bot_type, bot_id, pos_x, reply
    go_safe_all_finished = Signal(str, str, dict, str)  # source, bot_type, pos_x_dict, reply
    go_dance_motor_finished = Signal(str, str, int, int, str)  # source, bot_type, bot_id, cid, reply
    go_dance_bot_finished = Signal(str, str, int, str)  # source, bot_type, bot_id, reply
    go_dance_robot_finished = Signal(str, str)  # source, reply
    dance_travel = Signal(str, str, int, dict, float)  # source, bot_type, bot_id, motors_pos, ts
    # CURRENT_ERR
    current_error = Signal(str, int, int, bytes)
