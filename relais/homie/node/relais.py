"""
import settings

from homie.node.relay import Relais
from homie import HomieDevice

def main():
    homie = HomieDevice(settings)
    homie.add_node(Relay(pin=[2, 4]))
    homie.start()


main()
"""

from machine import Pin

from homie.node import HomieNode


ONOFF = {b'off': 0, b'on': 1, 0: b'off', 1: b'on'}


class Relais(HomieNode):

    def __init__(self, name="Relais", pin=(4,), interval=1):
        super().__init__(name=name, interval=interval)
        self.node_id = b"relais[]"
        self.has_new_update = True
        self.relais = []
        self.onoff = ONOFF

        # activate pins
        for p in pin:
            p = Pin(p, Pin.OUT, value=0)
            self.relais.append(p)

    def __str__(self):
        pass

    @property
    def subscribe(self):
        for relais in range(len(self.relais)):
            yield b'relais/relais_{}/power/set'.format(relais + 1)

    def get_properties(self):
        yield (b'relais/$type', b'relais')
        yield (b'relais/$properties', b"power")
        yield (b'relais/$array', '1-{}'.format(len(self.relais)))
        yield (b'relais/power/$settable', b"true")
        yield (b"relais/power/$datatype", b"boolean")

        for relais in len(self.relais):
            name = 'Relais {}'.format(relais + 1).encode()
            prop = b'relais/relais_{}'.format(relais + 1)
            yield (b'/'.join((prop, '/$name')), name)

    def callback(self, topic, message):
        relais = self.get_property_id_from_topic(topic) - 1
        self.relais[relais].value(self.onoff[message])
        self.has_new_update = True

    def has_update(self):
        if self.has_new_update is True:
            self.has_new_update = False
            return True
        return False

    def get_data(self):
        for relais in range(len(self.relais)):
            topic = b'relais/relais_{}/power'.format(relais + 1)
            yield (topic, self.onoff[self.relais[relais]()])
