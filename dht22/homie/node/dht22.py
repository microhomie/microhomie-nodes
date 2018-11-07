import dht

from machine import Pin

from homie.node import HomieNode


class DHT22(HomieNode):

    def __init__(self, name="Temp and Humi", pin=4, interval=60):
        super(DHT22, self).__init__(name=name, interval=interval)
        self.node_id = b"dht22"
        self.dht22 = dht.DHT22(Pin(pin))
        self.temperature = 0
        self.humidity = 0

    def __str__(self):
        return 'DHT22: Temperature = {}, Humidity = {}'.format(
            self.temperature, self.humidity)

    def get_properties(self):
        yield (b"dht22/$name", self.name)
        yield (b'dht22/$properties', b'temperature,humidity')

        # temperature
        yield (b'dht22/$type', b'temperature')
        yield (b'dht22/temperature/$name', b'Temperature')
        yield (b'dht22/temperature/$unit', b'°C')
        yield (b'dht22/temperature/$datatype', b'float')
        yield (b'dht22/temperature/$format', b'20.0:60')

        # humidity
        yield (b'dht22/$type', b'humidity')
        yield (b'dht22/humidity/$name', b'Humidity')
        yield (b'dht22/humidity/$unit', b'%')
        yield (b'dht22/humidity/$datatype', b'float')
        yield (b'dht22/humidity/$format', b'0:100')

    def update_data(self):
        self.dht22.measure()
        self.temperature = self.dht22.temperature()
        self.humidity = self.dht22.humidity()

    def get_data(self):
        yield (b'dht22/temperature', self.temperature)
        yield (b'dht22/humidity', self.humidity)
