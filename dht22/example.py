"""Example main.py for a Microhomie device with dht22 node"""

import utime
import settings

from homie.node.dht22 import DHT22
from homie import HomieDevice


homie = HomieDevice(settings)
homie.add_node(DHT22(pin=4))

homie.publish_properties()

while True:
    homie.publish_data()
    utime.sleep(1)
