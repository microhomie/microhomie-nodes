import dht

from machine import Pin

from homie.node import HomieNode
from homie import Property


class DHT22(HomieNode):

    def __init__(self, pin=4, interval=60):
        super(DHT22, self).__init__(interval=interval)
        self.dht22 = dht.DHT22(Pin(pin))
        self.temperature = 0
        self.humidity = 0

    def __str__(self):
        return 'DHT22: Temperature = {}, Humidity = {}'.format(
            self.temperature, self.humidity)

    def get_node_id(self):
        return [b'temperature', b'humidity']

    def get_properties(self):
        # temperature
        yield Property(b'temperature/$type', b'temperature', True)
        yield Property(b'temperature/$properties', b'degrees', True)
        yield Property(b'temperature/degrees/$settable', b'false', True)
        yield Property(b'temperature/degrees/$unit', b'°C', True)
        yield Property(b'temperature/degrees/$datatype', b'float', True)
        yield Property(b'temperature/degrees/$format', b'20.0:60', True)

        # humidity
        yield Property(b'humidity/$type', b'humidity', True)
        yield Property(b'humidity/$properties', b'percentage', True)
        yield Property(b'humidity/percentage/$settable', b'false', True)
        yield Property(b'humidity/percentage/$unit', b'%', True)
        yield Property(b'humidity/percentage/$datatype', b'float', True)
        yield Property(b'humidity/percentage/$format', b'0:100', True)

    def update_data(self):
        self.dht22.measure()
        self.temperature = self.dht22.temperature()
        self.humidity = self.dht22.humidity()

    def get_data(self):
        yield Property(b'temperature/degrees', self.temperature, True)
        yield Property(b'humidity/percentage', self.humidity, True)
