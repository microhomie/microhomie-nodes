"""
import utime
import settings

from homie.node.relay import Relay
from homie import HomieDevice


homie = HomieDevice(settings)
homie.add_node(Relay(pin=[2, 4]))

homie.publish_properties()

while True:
    homie.publish_data()
    homie.mqtt.check_msg()
    utime.sleep(0.5)
"""

from machine import Pin

from homie.node import HomieNode
from homie import Property


ONOFF = {b'off': 0, b'on': 1, 0: b'off', 1: b'on'}


class Relay(HomieNode):

    def __init__(self, pin=(4,), interval=1):
        super().__init__(interval=interval)
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
        for relay in range(len(self.relais)):
            relay += 1
            yield 'relay/relay_{}/set'.format(relay).encode()

    def get_node_id(self):
        return [b'relay[1-{}]'.format(len(self.relais))]

    def get_properties(self):
        relais = len(self.relais)
        properties_str = 'relay[1-{}]'.format(relais).encode()
        yield Property(b'relay/$type', b'relay', True)
        yield Property(b'relay/$properties', properties_str, True)

        for relay in range(relais):
            name = 'Relay {}'.format(relay + 1).encode()
            prop = 'relay/relay_{}'.format(relay + 1).encode()
            yield Property(prop + b'/$settable', b'true', True)
            yield Property(prop + b'/$name', name, True)
            yield Property(prop + b'/$datatype', b'string', True)
            yield Property(prop + b'/$format', b'on,off', True)

    def callback(self, topic, message):
        relay = self.get_property_id_from_topic(topic) - 1
        self.relais[relay].value(self.onoff[message])
        self.has_new_update = True

    def has_update(self):
        if self.has_new_update is True:
            self.has_new_update = False
            return True
        return False

    def get_data(self):
        for relay in range(len(self.relais)):
            topic = 'relay/relay_{}'.format(relay + 1).encode()
            yield Property(topic, self.onoff[self.relais[relay].value()], True)
