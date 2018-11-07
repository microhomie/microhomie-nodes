"""Example main.py for a Microhomie device with a switch node"""

import settings

from homie.node.switch import Switch
from homie.device import HomieDevice, utils


def main():
    # Network Setup
    utils.disable_ap()

    # Homie device setup
    homie = HomieDevice(settings)

    # Add LED node to device
    door = Switch(type="magnet", name="Stable door", pin=4)
    homie.add_node(door)

    # run forever
    homie.start()


main()
