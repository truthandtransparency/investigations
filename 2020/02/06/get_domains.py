#!/usr/bin/env python3

import json
import os
import requests
import yaml

from config import config

DEFAULT_HEADERS = {"Content-Type": "application/json", "apikey": config["token"]}
RESULTS_DIRECTORY = "{0}/{1}/domain_lists".format(os.path.expanduser("~"), config["results_dir"])

def get_domains(url, headers, server):
    domains = requests.get(url, params=headers)
    domain_page = json.loads(domains.text)
    write_domains(domain_page, server)
    if "meta" in domain_page.keys():
        get_domains("{0}/scroll/{1}".format(config["url"]["base"], domain_page["meta"]["scroll_id"]), DEFAULT_HEADERS, server)

def write_domains(domains, server):
    if not os.path.exists(RESULTS_DIRECTORY):
        os.makedirs(RESULTS_DIRECTORY)

    domain_file = open("{0}/{1}_domain_list.json".format(RESULTS_DIRECTORY, server), "a")
    domain_file.write("{0}\n".format(json.dumps(domains)))
    domain_file.close()

for server in config["current_name_servers"]:
    get_domains("{0}{1}".format(config["url"]["base"], config["url"]["list_domains"]), {"query": "ns='{0}'".format(server), **DEFAULT_HEADERS}, server)
