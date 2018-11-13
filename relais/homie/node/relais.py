"""
import settings

from homie.node.relay import Relais
from homie.device import HomieDevice

def main():
    homie = HomieDevice(settings)
    homie.add_node(Relay(pin=(2, 4))
    homie.start()


main()
"""

from machine import Pin

from homie.node import HomieNode


ONOFF = {b"false": 0, b"true": 1, 0: b"false", 1: b"true"}


class Relais(HomieNode):

    def __init__(self, name="Relais", pin=(4,), interval=1, value=0):
        super().__init__(name=name, interval=interval)
        self.node_id = b"relais[]"
        self.has_new_update = True
        self.relais = []

        # activate pins
        for p in pin:
            p = Pin(p, Pin.OUT, value=value)
            self.relais.append(p)

    def __str__(self):
        pass

    @property
    def subscribe(self):
        for r in range(len(self.relais)):
            yield 'relais/relais_{}/power/set'.format(r + 1).encode()

    def get_properties(self):
        yield (b'relais/$type', b'relais')
        yield (b'relais/$properties', b"power")
        yield (b'relais/$array', '1-{}'.format(len(self.relais)))
        yield (b'relais/power/$settable', b"true")
        yield (b"relais/power/$datatype", b"boolean")

        for r in range(len(self.relais)):
            name = 'Relais #{}'.format(r + 1)
            t = 'relais/relais_{}/$name'.format(r + 1).encode()
            yield (t, name)

    def callback(self, topic, message):
        r = self.get_property_id_from_set_topic(topic) - 1
        self.relais[r](ONOFF[message])
        self.has_new_update = True

    def has_update(self):
        if self.has_new_update is True:
            self.has_new_update = False
            return True
        return False

    def get_data(self):
        for r in range(len(self.relais)):
            t = 'relais/relais_{}/power'.format(r + 1).encode()
            yield (t, ONOFF[self.relais[r]()])
