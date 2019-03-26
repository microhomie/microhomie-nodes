import bme
from machine import Pin, I2C
from homie.node import HomieNode

class BME280(HomieNode):

    def __init__(self, name='Temp, Humi & Press', sda=4, sdc=5, frequency=100000, interval=60):
        super(BME280, self).__init__(name=name, interval=interval)
        self.node_id = b'bme280'
        i2c_if = I2C(scl=Pin(sdc), sda=Pin(sda), freq=frequency)
        self.bme280 = bme.BME280(i2c=i2c_if)
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0

    def __str__(self):
        return 'BME280: Temperature = {}, Humidity = {}, Pressure = {}'.format(
            self.temperature, self.humidity, self.pressure)

    def get_properties(self):
        yield (b"bme280/$name", self.name)
        yield (b'bme280/$type', b'BME280')
        yield (b'bme280/$properties', b'temperature,humidity,pressure')

        # temperature
        yield (b'bme280/temperature/$name', b'Temperature')
        yield (b'bme280/temperature/$unit', b'°C')
        yield (b'bme280/temperature/$datatype', b'float')
        yield (b'bme280/temperature/$format', b'-40:80')

        # humidity
        yield (b'bme280/humidity/$name', b'Humidity')
        yield (b'bme280/humidity/$unit', b'%')
        yield (b'bme280/humidity/$datatype', b'float')
        yield (b'bme280/humidity/$format', b'0:100')

        # pressure
        yield (b'bme280/pressure/$name', b'Pressure')
        yield (b'bme280/pressure/$unit', b'Pa')
        yield (b'bme280/pressure/$datatype', b'float')
        yield (b'bme280/pressure/$format', b'300:110000')

    def update_data(self):
        (temp, press, hum) = self.bme280.read_compensated_data()
        self.temperature = temp / 100
        self.humidity = hum / 1024
        self.pressure = press / 256

    def get_data(self):
        yield (b'bme280/temperature', self.temperature)
        yield (b'bme280/humidity', self.humidity)
        yield (b'bme280/pressure', self.pressure)
