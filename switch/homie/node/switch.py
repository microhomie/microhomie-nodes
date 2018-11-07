""""
Switch example, i.e. magnet reed switch for windows or doors.
"""

from machine import Pin

from homie.node import HomieNode


class Switch(HomieNode):

    def __init__(self, type, name="Switch", pin=4, interval=1):
        super().__init__(name=name, interval=interval)
        self.node_id = b"switch"
        self.switch = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.last_status = None

    def __repr__(self):
        return "Switch(type={!r}, name={!r}, property={!r}, interval={!r})".format(
            self.type, self.name, self.property, self.interval
        )

    def __str__(self):
        status = 'open' if self.is_open() else 'closed'
        return 'Switch is {}'.format(status)

    def is_open(self, as_str=False):
        return b"true" if self.switch() else b"false"

    def get_properties(self):
        yield (b'switch/$name', self.name)
        yield (b'switch/$type', self.type)
        yield (b'switch/$properties', b'open')
        yield (b'switch/open/$datatype', b'boolean')

    def has_update(self):
        status = self.switch()
        if status != self.last_status:
            self.last_status = status
            return True
        return False

    def get_data(self):
        yield (b'switch/open', self.is_open())
