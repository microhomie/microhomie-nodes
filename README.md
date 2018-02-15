# Nodes for the Homie v2 MicroPython Framework

For full instruction see the Microhomie repository at https://github.com/microhomie/micropython-homie.

This repository has a lot of pre written nodes for Microhomie the MicroPython implementation of the [Homie v2](https://github.com/marvinroger/homie) convention.

Most of these nodes can be used out of the box to publish data. 

# Installation

You have to setup/configure the network by yourself.

You can also install the `micropython-homie-nodes` package from PyPi with all the nodes we have for you:

```python
>>> import upip
>>> upip.install('micropython-homie-nodes')
```

# Example with DHT22
If you want to use a DHT22 sensor as an example wire it up according to `homie/node/dht22.png`, copy the files `__init__.py` and `dht22.py` from `homie/node` to the `lib/homie/node` directory on your device. You will find an example main.py for a dht22 setup in this gist: https://gist.github.com/kinkerl/5c76558652e4102716180dede30b0a5f 
Copy this example to `main.py` on your device and on next reset it starts publishing temperature and humidity.


