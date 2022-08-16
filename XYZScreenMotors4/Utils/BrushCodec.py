from XYZUtil4.tools.for_class import singleton


@singleton
class _Code:
    HEAD = b'\xeb'
    FUNC = b'\x20'
    RUN_ONCE = b'\x02'
    CMD = b'\xeb\x20\x5a\x10\x68'


CODEC = _Code()
