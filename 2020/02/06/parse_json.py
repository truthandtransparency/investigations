#!/usr/bin/env python3

import json
import os

from config import config

RESULTS_DIRECTORY = "{0}/{1}/domain_lists".format(os.path.expanduser("~"), config["results_dir"])
DOMAIN_LIST_FILE = "{0}/{1}/unique_domains.txt".format(os.path.expanduser("~"), config["results_dir"])

domains = []

for filename in os.listdir(RESULTS_DIRECTORY):
    with open("{0}/{1}".format(RESULTS_DIRECTORY, filename)) as json_data:
        for blob in json_data:
            d = json.loads(blob)
            if "records" in d.keys():
                for record in d["records"]:
                    domains.append(record["hostname"])

with open(DOMAIN_LIST_FILE, "w") as domain_file:
    for domain in sorted(set(domains)):
        domain_file.write("{0}\n".format(domain))
