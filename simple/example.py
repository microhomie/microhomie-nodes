"""Example main.py for a Microhomie device with a simple node"""
import utime
import settings

from homie.node.simple import SimpleHomieNode
from homie.device import HomieDevice


def main():
    homie = HomieDevice(settings)

    n = SimpleHomieNode(node_type=b'dummy', node_property=b'value', interval=5)
    n.value = 17

    homie.add_node(n)
    homie.publish_properties()

    while True:
        homie.publish_data()
        n.value = utime.time()
        print(n)
        utime.sleep(1)


main()
