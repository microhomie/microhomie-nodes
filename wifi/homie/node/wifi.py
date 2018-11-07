from homie.node import HomieNode
from homie import utils


class Wifi(HomieNode):
    def __init__(self, ssid, interval=60):
        super().__init__(name="", interval=interval)
        self.node_id = b"$stats"
        self.ssid = ssid.encode('utf-8')
        self.rssi = 0

    def __repr__(self):
        return "Wifi(ssid={!r}, interval={!r})".format(
            self.ssid.decode(), self.interval
        )

    def __str__(self):
        return 'WIFI: rssi = {}'.format(self.rssi)

    def update_data(self):
        ssids = utils.wlan.scan()
        for ssid in ssids:
            if ssid[0] == self.ssid:
                self.rssi = ssid[3]

    def get_data(self):
        yield (b'$stats/signal', self.rssi)
