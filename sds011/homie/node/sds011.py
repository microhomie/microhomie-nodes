# -*- coding: utf-8 -*-
"""Node for the SDS011 airquality sensor with the UART protocoll.

This node only works for micropython on the ESP32. As of this writing,
the ESP8266 implementation of micropython does not implement the required
UART functions.


Inspired by https://github.com/g-sam/polly


Wiring of the sensor works as follows:

SDS011  --  ESP32

TX      --  RX (16)
RX      --  TX (17)
5v      --  5v
GND     --  GND


"""

import machine
import ustruct as struct
import sys
import utime as time
from homie.node import HomieNode


CMDS = {'SET': b'\x01',
        'GET': b'\x00',
        'DUTYCYCLE': b'\x08',
        'SLEEPWAKE': b'\x06'}


class SDS011(HomieNode):

    def __init__(self, name="Air sensor", interval=60, allowed_time=20, rx=16, tx=17):
        super(SDS011, self).__init__(name=name, interval=interval)
        self.node_id = b"sds011"
        self.pm25 = 0
        self.pm10 = 0
        self.packet_status = True
        self.allowed_time = allowed_time
        self.uart = machine.UART(2, baudrate=9600, rx=rx, tx=tx, timeout=10, bits=8, parity=None, stop=1)

    def __str__(self):
        return 'SDS011: PM 2.5 = {}, PM 10 = {}'.format(self.pm25, self.pm10)

    def get_node_id(self):
        return [b'pm25', b'pm10', b'packet_status']

    def get_properties(self):
        yield (b'sds011/$name', b'Air sensor')
        yield (b'sds011/$type', b'SDS011')
        yield (b'sds011/$properties', b'pm25,pm10,packet_status')

        yield (b'sds011/pm25/$unit', b'mg/m3')
        yield (b'sds011/pm25/$datatype', b'float')
        yield (b'sds011/pm25/$format', b'20.0:60')

        yield (b'sds011/pm10/$unit', b'mg/m3')
        yield (b'sds011/pm10/$datatype', b'float')
        yield (b'sds011/pm10/$format', b'20.0:60')

        yield (b'sds011/packet_status/$datatype', b'string')
        yield (b'sds011/packet_status/$format', b'valid,invalid')

    def get_data(self):
        yield (b'sds011/pm25', self.pm25)
        yield (b'sds011/pm10', self.pm10)
        yield (b'sds011/packet_status', self.packet_status)

    def make_command(self, cmd, mode, param):
        header = b'\xaa\xb4'
        padding = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff'
        checksum = chr((ord(cmd) + ord(mode) + ord(param) + 255 + 255) % 256)
        tail = b'\xab'
        return header + cmd + mode + param + padding + bytes(checksum, 'utf8') + tail

    def wake(self):
        cmd = self.make_command(CMDS['SLEEPWAKE'], CMDS['SET'], chr(1))
        print('Sending wake command to sds011:', cmd)
        self.uart.write(cmd)

    def sleep(self):
        cmd = self.make_command(CMDS['SLEEPWAKE'], CMDS['SET'], chr(0))
        print('Sending sleep command to sds011:', cmd)
        self.uart.write(cmd)

    def update_data(self):
        self.wake()
        start_time = time.ticks_ms()
        delta_time = 0
        while (delta_time <= self.allowed_time * 1000):
            try:
                header = self.uart.read(1)
                if header == b'\xaa':
                    command = self.uart.read(1)
                    if command == b'\xc0':
                        packet = self.uart.read(8)
                        *data, checksum, tail = struct.unpack("<HHBBBs", packet)

                        # verify packet
                        checksum_OK = checksum == (sum(data) % 256)
                        tail_OK = tail == b'\xab'

                        self.pm25 = data[0]/10.0
                        self.pm10 = data[1]/10.0
                        self.packet_status = b"valid" if (checksum_OK and tail_OK) else b"invalid"

                    elif command == b'\xc5':
                        packet = self.uart.read(8)
                        print('Reply received but not implemented:', packet)
                delta_time = time.ticks_diff(time.ticks_ms(), start_time) if self.allowed_time else 0
            except Exception as e:
                print('Problem attempting to read:', e)
                sys.print_exception(e)
        self.sleep()
