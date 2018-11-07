"""Example main.py for a Microhomie device with dht22 node"""

import settings

from homie.node.dht22 import DHT22
from homie import HomieDevice


def main():
    homie = HomieDevice(settings)
    homie.add_node(DHT22(pin=4))

    homie.publish_properties()

    homie.start()


main()
