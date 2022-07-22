from XYZScreenMotors4.Utils._Network import Network
from XYZScreenMotors4.Utils.BrushCodec import CODEC


class OneWiper:
    def __init__(self, wiper_id: int, mcu_addr: tuple):
        self.wiper_id = wiper_id
        self._network = Network(side_id=wiper_id, mcu_ip=mcu_addr[0], mcu_port=mcu_addr[1])

    # API
    def brush_once(self):
        self._network.send(data=CODEC.HEAD + CODEC.FUNC + CODEC.RUN_ONCE)
