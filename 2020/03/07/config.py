#!/usr/bin/env python3

import yaml
from os.path import expanduser

with open("{0}/config.yaml".format(expanduser("~")), "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)
