class _Head:

    ERROR = b'\xee'
    TO_MCU = b'\xeb'
    ECHO_MCU = b'\xaa'
    REACHED = b'\xbb'
    FROM_MCU = b'\x70'
    TEMPERATURE_HUMIDITY = b'\x71'
    HARD_RESET = b'\x72'
    START_DANCE = b'\x73'


class _Mode:

    SPD = b'\x01'
    POS = b'\x02'
    OFF = b'\x03'


class _PowerOff:
    WRITE = b'\x01'
    READ = b'\x02'


class _Reached:
    MOVE = b'\xb2'
    DANCE = b'\xb1'


class _Codec:

    HEAD = _Head()

    # MATH_MOTOR
    SET_MATH_PORT = b'\xfe'
    SET_TURBO = b'\xff'
    SET_SAFE = b'\xfe'

    # CONF
    SET_RANGE1 = b'\x01'
    SET_RANGE0 = b'\x02'

    # POWER_OFF
    CHECK_POWER_OFF = b'\x03'
    POWER_OFF = _PowerOff()

    # PID
    POS_GAIN = b'\x05'

    # HOMING
    HOMING_HEAD = b'\x30'
    HOMING = b'\x01'
    ORG = b'\x02'
    HOMING_FINISHED = b'\01'

    # REACHED
    REACHED = _Reached()

    # DANCE
    GO_DANCE = b'\x66'
    ACKNOWLEDGE_DANCE = b'\x02'

    # MODE
    SET_MODE = b'\x20'
    MOVE_TO_SPD = b'\x21'
    MOVE_TO_POS = b'\x60'
    MODE = _Mode()


CODEC = _Codec()
