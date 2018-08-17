from machine import Pin

from homie.node import HomieNode
from homie import Property


class PIR(HomieNode):

    def __init__(self, pin=4, interval=1):
        super().__init__(interval=interval)
        self.pir = Pin(pin, Pin.IN, pull=Pin.PULL_UP)
        self.last_pir_state = 0

    def __str__(self):
        return 'Last PIR State = {}'.format(self.last_pir_state)

    def get_node_id(self):
        return [b'pir']

    def get_properties(self):
        yield Property(b'pir/$type', b'pir', True)
        yield Property(b'pir/$properties', b'motion', True)
        yield Property(b'pir/motion/$settable', b'false', True)
        yield Property(b'pir/motion/$datatype', b'boolean', True)
        yield Property(b'pir/motion/$format', b'true,false', True)

    def has_update(self):
        new_pir_state = self.pir.value()
        if new_pir_state != self.last_pir_state:
            self.last_pir_state = new_pir_state
            return True
        return False

    def get_data(self):
        payload = 'true' if self.last_pir_state == 1 else 'false'
        yield Property(b'pir/motion', payload, True)
