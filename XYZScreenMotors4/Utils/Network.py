from XYZUtil4.network.UDP import UDP


# IP/PORT 从utils的config里读取
class Network:

    def __init__(self, side_id: int, mcu_ip: str, mcu_port: int):
        self._side_id = side_id
        self._mcu_ip = mcu_ip
        self._mcu_port = mcu_port
        self.udp = UDP(is_nuc=True)
        self.udp.sign_is_online.connect(self._signal_udp_is_online)
        self.udp.set_peer_address(address=(mcu_ip, mcu_port))
        self._read_count = 0
        self._write_count = 0

    def _signal_udp_is_online(self, ip: str, port: int, is_online: bool):
        print(f'雨刷器上线了， ONLIE={is_online}')

    def send(self, data: bytes, is_resent_cmd: bool = False):
        self.udp.send_to(data=data, ip=self._mcu_ip, port=self._mcu_port, is_resent_command=is_resent_cmd)
        self._write_count += 1
        self._write_count = 0 if self._write_count == 256 else self._write_count

    def get_read_count(self) -> int:
        return self._read_count

    def get_write_count(self) -> int:
        return self._write_count

    def exit(self):
        self.udp.exit()
