from machine import Pin

from homie.node import HomieNode


class PIR(HomieNode):

    def __init__(self, name="Motion sensor", pin=4, interval=1):
        super().__init__(interval=interval, name=name)
        self.node_id = b"pir"
        self.pir = Pin(pin, Pin.IN, pull=Pin.PULL_UP)
        self.name = name
        self.latest = 0

    def __str__(self):
        return 'Last PIR State = {}'.format(self.latest)

    def get_properties(self):
        yield (b"pir/$name", self.name)
        yield (b'pir/$type', b'pir')
        yield (b'pir/$properties', b'motion')
        yield (b"pir/motion/$name", b"PIR sensor")
        yield (b'pir/motion/$retained', b'false')
        yield (b'pir/motion/$datatype', b'boolean')
        yield (b'pir/motion/$format', b'true,false')

    def has_update(self):
        new = self.pir()
        if new != self.latest:
            self.latest = new
            return True
        return False

    def get_data(self):
        payload = b'true' if self.latest == 1 else b'false'
        yield (b'pir/motion', payload, False)
