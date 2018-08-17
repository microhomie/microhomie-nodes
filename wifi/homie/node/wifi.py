from homie.node import HomieNode
from homie import Property, utils


class Wifi(HomieNode):
    def __init__(self, ssid, interval=60):
        super().__init__(interval=interval)
        self.ssid = ssid.encode('utf-8')
        self.rssi = 0

    def __str__(self):
        return 'WIFI: rssi = {}'.format(self.rssi)

    def get_node_id(self):
        return []

    def get_properties(self):
        return ()

    def update_data(self):
        ssids = utils.wlan.scan()
        for ssid in ssids:
            if ssid[0] == self.ssid:
                self.rssi = ssid[3]

    def get_data(self):
        yield Property(b'$stats/signal', self.rssi, True)
