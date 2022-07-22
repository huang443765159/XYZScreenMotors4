from XYZUtil4.tools.for_class import singleton


@singleton
class _Code:
    HEAD = b'\xeb'
    FUNC = b'\x20'
    RUN_ONCE = b'\x02'


CODEC = _Code()
