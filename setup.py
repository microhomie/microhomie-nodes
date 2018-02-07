from setuptools import setup
import sdist_upip


setup(
    name='micropython-homie-nodes',
    version='0.1.0',
    description='Nodes for the Homie v2 MicroPython Framework.',
    long_description='More documentation is available at https://github.com/microhomie/micropython-homie',
    url='https://github.com/microhomie/micropython-homie-nodes',
    author='Microhomie Developers',
    author_email='contact@microhomie.com',
    maintainer='Microhomie Developers',
    maintainer_email='contact@microhomie.com',
    license='MIT',
    cmdclass={'sdist': sdist_upip.sdist},
    packages=['homie.node'],
    install_requires=['micropython-homie'],
)
