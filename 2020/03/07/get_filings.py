#!/usr/bin/env python3

import json
import os
import requests
import yaml

from config import config

DEFAULT_HEADERS = {"Content-Type": "application/json"}
RESULTS_DIRECTORY = "{0}/{1}".format(os.path.expanduser("~"), config["results_dir"])

def get_filings(url, headers):
    return json.loads(requests.get(url, params=headers).text)

def write_filings(filings, cik):
    for filing in filings['results']:
        results_dir = "{0}/{1}/{2}".format(RESULTS_DIRECTORY,filing,cik)
        
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        results_file = open("{0}/{1}".format(results_dir, config["holdings_filename"]), "w")
        results_file.write("{0}\n".format(json.dumps(filings["results"][filing])))
        results_file.close()

for cik in config["ciks"]:
    filings = get_filings("{0}{1}".format(config["url"]["base"], cik), {**DEFAULT_HEADERS})
    write_filings(filings, cik)
