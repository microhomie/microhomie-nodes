"""Example main.py for a Microhomie device with led node"""
import settings

from homie.node.led import LED
from homie.device import HomieDevice, utils


def main():
    # Network Setup
    utils.disable_ap()

    # Homie device setup
    homie = HomieDevice(settings)

    # Add LED node to device
    homie.add_node(LED(pin=2))

    # run forever
    homie.start()


main()
