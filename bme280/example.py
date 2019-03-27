"""Example main.py for a Microhomie device with bme280 node"""

import settings
from homie.node.bme280 import BME280
from homie.device import HomieDevice

def main():
    homie_dev = HomieDevice(settings)
    homie_dev.add_node(BME280())
    homie_dev.publish_properties()
    homie_dev.start()

main()
