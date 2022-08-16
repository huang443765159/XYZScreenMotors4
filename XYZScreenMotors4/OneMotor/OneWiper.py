import time
import threading

from XYZScreenMotors4.Utils.Network import Network
from XYZScreenMotors4.Utils.BrushCodec import CODEC


class OneWiper:
    def __init__(self, wiper_id: int, mcu_addr: tuple):
        self.wiper_id = wiper_id
        self._network = Network(side_id=wiper_id, mcu_ip=mcu_addr[0], mcu_port=mcu_addr[1])
        self._is_loop = False
        self._link = False

    def _brush_loop(self):
        while self._is_loop:
            self.brush_once()
            time.sleep(20)

    # API
    def brush_once(self):
        if self._link:
            self._network.send(data=CODEC.CMD)

    def brush_loop(self):
        thread = threading.Thread(target=self._brush_loop, daemon=True)
        self._is_loop = True
        thread.start()

    def set_link(self, link: bool):
        self._link = link

    def get_link(self) -> bool:
        return self._link

    def stop(self):
        self._is_loop = False
