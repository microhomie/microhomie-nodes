#!/usr/bin/env python3
# MICROHOMIE will pick up glob from the current dir otherwise.
import sys
sys.path.pop(0)

import glob


TEMPLATE = """\
import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system's.
sys.path.pop(0)
from setuptools import setup
sys.path.append("..")
import sdist_upip

setup(name='microhomie-node-%(dist_name)s',
      version='%(version)s',
      description=%(desc)r,
      long_description=%(long_desc)s,
      url='https://github.com/microhomie/microhomie-nodes',
      author=%(author)r,
      author_email=%(author_email)r,
      maintainer=%(maintainer)r,
      maintainer_email='contact@microhomie.com',
      license=%(license)r,
      cmdclass={'sdist': sdist_upip.sdist},
      %(_what_)s=[%(modules)s]%(_inst_req_)s)
"""

MICROHOMIE_NODE_DESC = """\
This is a node implementation for a Microhomie device.
"""

MICROHOMIE_DEVELS = 'Microhomie Developers'
MICROHOMIE_DEVELS_EMAIL = 'contact@microhomie.com'


def parse_metadata(f):
    data = {}
    for l in f:
        l = l.strip()
        if l[0] == "#":
            continue
        k, v = l.split("=", 1)
        data[k.strip()] = v.strip()
    return data


def write_setup(fname, substs):
    with open(fname, "w") as f:
        f.write(TEMPLATE % substs)


def main():
    for fname in glob.iglob("*/metadata.txt"):
        print(fname)
        with open(fname) as f:
            data = parse_metadata(f)

        dirname = fname.split("/")[0]
        module = dirname
        data["_what_"] = "packages"

        if "author" not in data:
            data["author"] = MICROHOMIE_DEVELS
        if "author_email" not in data:
            data["author_email"] = MICROHOMIE_DEVELS_EMAIL
        if "maintainer" not in data:
            data["maintainer"] = MICROHOMIE_DEVELS
        if "desc" not in data:
            data["desc"] = "%s node for Microhomie" % module
        if "long_desc" not in data:
            data["long_desc"] = MICROHOMIE_NODE_DESC
        if "license" not in data:
            data["license"] = "MIT"


        if "dist_name" not in data:
            data["dist_name"] = dirname
        if "name" not in data:
            data["name"] = module
        if data["long_desc"] in ("README", "README.rst"):
            data["long_desc"] = "open(%r).read()" % data["long_desc"]
        else:
            data["long_desc"] = repr(data["long_desc"])

        # data["modules"] = "'homie.node." + data["name"].rsplit(".", 1)[0] + "'"
        data["modules"] = "'homie.node'"
        if "extra_modules" in data:
            data["modules"] += ", " + ", ".join(["'" + x.strip() + "'" for x in data["extra_modules"].split(",")])

        if "depends" in data:
            deps = [x.strip() for x in data["depends"].split(",")]
            deps.append('microhomie')
        else:
            deps = ['microhomie']
        data["_inst_req_"] = ",\n      install_requires=['" + "', '".join(deps) + "']"

        write_setup(dirname + "/setup.py", data)


if __name__ == "__main__":
    main()
