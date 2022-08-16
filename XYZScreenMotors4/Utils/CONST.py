from XYZUtil4.tools.for_class import singleton


@singleton
class _Const:
    WIPER_ADDR = ('192.168.50.236', 54188)


CONST = _Const()
