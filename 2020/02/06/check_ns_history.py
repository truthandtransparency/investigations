#!/usr/bin/env python3

import json
import logging
import os
import requests

from config import config

LOGGING_DIRECTORY = "{0}/{1}".format(os.path.expanduser("~"), config["log_dir"])
RESULTS_DIRECTORY = "{0}/{1}/domains_found".format(os.path.expanduser("~"), config["results_dir"])
DOMAIN_LIST_FILE = "{0}/{1}/unique_domains.txt".format(os.path.expanduser("~"), config["results_dir"])

def get_ns_history(domain,record_type):
    url = "{0}/history/{1}/dns/{2}".format(config["url"]["base"],domain,record_type)
    history = requests.get(url, params={"Content-Type": "application/json", "apikey": config["token"]})
    try:
        history.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error("ERROR RETRIEVING HISTORY FOR {0}: {1}".format(domain, str(e)))
        return None
    else:
        logging.info("Successfully retrieved history for {0}.".format(domain))
        return json.loads(history.text)

def check_ns_history(history):
    if history is not None:
        for record in history["records"]:
            for value in record["values"]:
                if config["previous_name_server_parent"] in value["nameserver"]:
                    save_ns_history(history)

def save_ns_history(history):
    if not os.path.exists(RESULTS_DIRECTORY):
        os.makedirs(RESULTS_DIRECTORY)

    history_file = open("{0}/{1}.json".format(RESULTS_DIRECTORY, history["endpoint"].split("/")[3]), "w")
    history_file.write(json.dumps(history))
    history_file.close()

if not os.path.exists(LOGGING_DIRECTORY):
    os.makedirs(LOGGING_DIRECTORY)

logging.basicConfig(filename="{0}/log.log".format(LOGGING_DIRECTORY), filemode="a", format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

with open(DOMAIN_LIST_FILE, "r") as domain_list:
    for domain in domain_list:
        check_ns_history(get_ns_history(domain.rstrip(), "ns"))
